# -*- coding: utf-8 -*-
import csv, glob, os, sys
io_enc = 'utf-8-sig'
d = r'E:\ai-project\E-commerce-ai\documents\job-research-2026-10\data'
files = sorted(glob.glob(os.path.join(d, '*_20261029.csv')))
out = []
out.append('files found: %d' % len(files))
for f in files:
    rows = list(csv.DictReader(open(f, encoding=io_enc)))
    cols = list(rows[0].keys())
    empt = {c: sum(1 for r in rows if not (r.get(c) or '').strip()) for c in cols}
    dup = len(rows) - len(set((r['company'], r['job_title']) for r in rows))
    bad = {k: v for k, v in empt.items() if v}
    out.append('%s | rows=%d | cols=%d | dup=%d | empty=%s' % (os.path.basename(f), len(rows), len(cols), dup, bad))
open(os.path.join(os.path.dirname(__file__), 'verify_out.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
