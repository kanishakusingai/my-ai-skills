#!/usr/bin/env python3
"""Merge Helium 10 Xray/Cerebro keyword CSVs: dedupe and rank.
Usage: merge_xray.py file1.csv file2.csv ... [--top N]"""
import argparse, re, sys
import pandas as pd

def first_num(s):
    m = re.findall(r'[\d.]+', str(s).replace(',', ''))
    return float(m[0]) if m else None

p = argparse.ArgumentParser()
p.add_argument('files', nargs='+')
p.add_argument('--top', type=int, default=300)
a = p.parse_args()

frames = []
for i, f in enumerate(a.files):
    d = pd.read_csv(f, encoding='utf-8-sig')
    d['src'] = i
    frames.append(d)
d = pd.concat(frames)
cols = {c.lower(): c for c in d.columns}
def col(*names):
    for n in names:
        for k, v in cols.items():
            if n in k:
                return v
    return None
kw = col('keyword phrase', 'keyword')
sv = col('search volume')
bid = col('suggested ppc bid', 'ppc')
cp = col('competing products')
rk = col('organic rank')
if not kw:
    sys.exit('No keyword column found. Columns: %s' % list(d.columns))
d['_bid'] = d[bid].map(first_num) if bid else None
d['_sv'] = pd.to_numeric(d[sv].astype(str).str.replace(',', ''), errors='coerce') if sv else None
d['_cp'] = pd.to_numeric(d[cp].astype(str).str.replace(',', ''), errors='coerce') if cp else None
d['_rk'] = pd.to_numeric(d[rk], errors='coerce') if rk else None
g = d.groupby(kw).agg(search_volume=('_sv', 'max'), suggested_bid=('_bid', 'max'),
                      competing_products=('_cp', 'max'), competitors_ranking=('src', 'nunique'),
                      best_rank=('_rk', 'min')).reset_index().rename(columns={kw: 'keyword'})
g = g.sort_values(['competitors_ranking', 'search_volume'], ascending=False).head(a.top)
pd.set_option('display.width', 220, 'display.max_rows', 1000, 'display.max_colwidth', 60)
print(g.to_string(index=False))
