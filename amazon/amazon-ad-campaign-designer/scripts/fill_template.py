#!/usr/bin/env python3
"""Fill the Amazon bulk keyword template.
Usage: fill_template.py --template keyword_template.xlsx --match Exact --out out.xlsx --kw "car vacuum cleaner:11" --kw "..."
Or: --csv keywords.csv with columns keyword,bid"""
import argparse, csv, openpyxl
import math
p = argparse.ArgumentParser()
p.add_argument('--template', required=True)
p.add_argument('--match', required=True, choices=['Exact', 'Phrase', 'Broad'])
p.add_argument('--out', required=True)
p.add_argument('--kw', action='append', default=[], help='keyword:bid')
p.add_argument('--csv')
a = p.parse_args()
rows = []
for s in a.kw:
    k, b = s.rsplit(':', 1)
    rows.append((k.strip(), float(b)))
if a.csv:
    for r in csv.DictReader(open(a.csv, encoding='utf-8-sig')):
        rows.append((r['keyword'].strip(), float(r['bid'])))
seen, clean = set(), []
for k, b in rows:
    if k.lower() not in seen:
        seen.add(k.lower()); clean.append((k, b))
wb = openpyxl.load_workbook(a.template)
ws = wb['Data'] if 'Data' in wb.sheetnames else wb.active
if [ws.cell(4, c).value for c in (1, 2, 3)] != ['Keyword', 'Match Type', 'Bid']:
    raise SystemExit('Expected Keyword / Match Type / Bid headers in row 4')
if not clean or any(not k or not math.isfinite(b) or b <= 0 for k, b in clean):
    raise SystemExit('Provide non-empty keywords and positive finite numeric bids')
for row in ws.iter_rows(min_row=5, max_row=max(ws.max_row, 5), max_col=3):
    for cell in row:
        cell.value = None
for i, (k, b) in enumerate(clean, start=5):
    ws.cell(i, 1, k); ws.cell(i, 2, a.match); ws.cell(i, 3, int(b) if b == int(b) else b)
wb.save(a.out)
print('Wrote %d %s keywords to %s' % (len(clean), a.match, a.out))
