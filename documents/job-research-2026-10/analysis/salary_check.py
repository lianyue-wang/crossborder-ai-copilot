# -*- coding: utf-8 -*-
import csv, re, glob, os, statistics
d = r'E:\ai-project\E-commerce-ai\documents\job-research-2026-10\data'
def parse_salary(s):
    s = s.strip()
    if not s: return None
    # 日薪
    m = re.match(r'([\d.]+)\s*[-~]\s*([\d.]+)\s*元/天', s)
    if m: return (float(m.group(1))+float(m.group(2)))/2 * 22 / 1000  # 折算万/月
    # 年薪
    m = re.match(r'([\d.]+)\s*[-~]\s*([\d.]+)\s*万/年', s)
    if m: return (float(m.group(1))+float(m.group(2)))/2 / 12
    # 月薪 X-YK 或 X-Y万
    m = re.match(r'([\d.]+)\s*[-~]\s*([\d.]+)\s*[Kk]', s)
    if m: return (float(m.group(1))+float(m.group(2)))/2 / 10
    m = re.match(r'([\d.]+)\s*[-~]\s*([\d.]+)\s*万', s)
    if m: return (float(m.group(1))+float(m.group(2)))/2
    return None

first_tier = ('北京','上海','深圳','广州','杭州')
rows_all = []
for f in glob.glob(os.path.join(d, 'boss_*_20261029.csv')):
    for r in csv.DictReader(open(f, encoding='utf-8-sig')):
        rows_all.append(r)
out = []
yt = [r for r in rows_all if any(c in r.get('city','') for c in first_tier)]
out.append('Boss一线行数: %d' % len(yt))
g13 = []
for r in yt:
    sal = parse_salary(r['salary'])
    if sal is None:
        out.append('  未解析: %s | %s | %s | %s' % (r['job_title'][:20], r['city'], r['salary'], r['experience']))
        continue
    if '1-3' in r.get('experience',''):
        g13.append((sal, r['job_title'][:18], r['city'], r['salary'], r['experience']))
g13.sort()
out.append('一线1-3年样本数: %d' % len(g13))
for x in g13: out.append('  %.2f万 | %s | %s | %s | %s' % x)
if g13:
    out.append('一线1-3年中位: %.3f' % statistics.median([x[0] for x in g13]))
open(r'E:\ai-project\E-commerce-ai\documents\job-research-2026-10\analysis\salary_check.txt','w',encoding='utf-8').write('\n'.join(out))
print('done')
