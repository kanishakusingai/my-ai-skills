#!/usr/bin/env python3
"""Check negatives don't block your own keywords.
Usage: check_negatives.py --positives pos.txt --neg-exact ne.txt --neg-phrase np.txt
(each file: one keyword per line)"""
import argparse, re, sys
def load(p): return [l.strip().lower() for l in open(p, encoding='utf-8') if l.strip()]
p = argparse.ArgumentParser()
p.add_argument('--positives', required=True)
p.add_argument('--neg-exact', required=True)
p.add_argument('--neg-phrase', required=True)
a = p.parse_args()
pos, ne, nph = load(a.positives), set(load(a.neg_exact)), load(a.neg_phrase)
bad = 0
for k in pos:
    if k in ne:
        print('BLOCKED (negative exact = positive): %s' % k); bad += 1
    for n in nph:
        if re.search(r'(?<!\w)%s(?!\w)' % re.escape(n), k):
            print('BLOCKED (negative phrase "%s" inside positive): %s' % (n, k)); bad += 1
sys.exit(1 if bad else print('OK: no negative blocks a positive keyword') or 0)
