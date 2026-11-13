# -*- coding: utf-8 -*-
import csv
f = r'E:\ai-project\E-commerce-ai\documents\job-research-2026-10\analysis\可投岗位清单_剔除全栈版_20261029.csv'
rows = list(csv.DictReader(open(f, encoding='utf-8-sig')))
big = ['华为','字节','腾讯','阿里','美团','百度','京东','网易','小米','中兴','OPPO','vivo','拼多多','快手','大疆','蚂蚁','滴滴','比亚迪']
bad_big = [r for r in rows if any(b in r.get('公司','') for b in big)]
edu_bad = [r for r in rows if r.get('学历','') not in ('不限','大专','大专及以上')]
cd = [r for r in rows if '成都' in r.get('城市','')]
out = []
out.append('rows=%d' % len(rows))
out.append('误含大厂=%d' % len(bad_big))
out.append('学历不符合=%d 样例:%s' % (len(edu_bad), [r.get('学历') for r in edu_bad[:5]]))
out.append('成都条数=%d' % len(cd))
out.append('平台分布: Boss=%d 51job=%d' % (sum(1 for r in rows if 'Boss' in r.get('平台','')), sum(1 for r in rows if '51job' in r.get('平台',''))))
out.append('学历取值集合: %s' % sorted(set(r.get('学历','') for r in rows)))
open(r'E:\ai-project\E-commerce-ai\documents\job-research-2026-10\analysis\appliable_check2.txt','w',encoding='utf-8').write('\n'.join(out))
