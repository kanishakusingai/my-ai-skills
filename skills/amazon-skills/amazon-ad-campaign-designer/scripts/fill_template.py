#!/usr/bin/env python3
"""Fill the Amazon bulk keyword template.
Usage: fill_template.py --template keyword_template.xlsx --match Exact --out out.xlsx --kw "car vacuum cleaner:11" --kw "..."
Or: --csv keywords.csv with columns keyword,bid"""
import argparse, csv, openpyxl
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
for i, (k, b) in enumerate(clean, start=5):
    ws.cell(i, 1, k); ws.cell(i, 2, a.match); ws.cell(i, 3, int(b) if b == int(b) else b)
wb.save(a.out)
print('Wrote %d %s keywords to %s' % (len(clean), a.match, a.out))
