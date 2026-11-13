# -*- coding: utf-8 -*-
"""剔除全栈版：仅统计 ai_dev + agent_dev 共4个文件（435条纯AI岗位）"""
import csv, json, os, statistics, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stats as S

BASE = r"E:\ai-project\E-commerce-ai\documents\job-research-2026-10"
DATA = os.path.join(BASE, "data")
ANA = os.path.join(BASE, "analysis")

FILES = [
    "boss_ai_dev_20261027.csv",
    "boss_agent_dev_20261027.csv",
    "51job_ai_dev_20261027.csv",
    "51job_agent_dev_20261027.csv",
]

rows = []
for fn in FILES:
    with open(os.path.join(DATA, fn), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if not r.get("job_title"): continue
            r["__file"] = fn
            r["platform"] = r["platform"].strip()
            r["__kw"] = S.keyword_of(fn)
            rows.append(r)

n = len(rows)
out = {"样本量": n, "文件": {}}
for fn in FILES:
    out["文件"][fn] = sum(1 for r in rows if r["__file"] == fn)

def pct(x): return S.pct(x, n)

# 城市分组
cg = Counter(S.city_group(r["city"]) for r in rows)
out["城市分组"] = {k: {"计数": v, "占比%": pct(v)} for k, v in cg.most_common()}

# 学历
edu = Counter(S.norm_education(r["education"]) for r in rows)
out["学历分布"] = {k: {"计数": edu.get(k, 0), "占比%": pct(edu.get(k, 0))}
                   for k in ["不限","大专","大专及以上","本科","硕士","博士","未标注","其他"] if edu.get(k, 0)}

# 经验
exp = Counter(S.norm_experience(r["experience"]) for r in rows)
out["经验分布"] = {k: {"计数": exp.get(k, 0), "占比%": pct(exp.get(k, 0))}
                  for k in S.EXP_BUCKETS + ["其他"] if exp.get(k, 0)}

# 技能TOP20
sc = Counter()
for r in rows:
    for s in S.skills_hit(r):
        sc[s] += 1
out["技能TOP20"] = [{"技能": k, "命中": v, "占比%": pct(v)} for k, v in sc.most_common(20)]

# 职责TOP10
dc = Counter()
for r in rows:
    for d in S.duty_hit(r):
        dc[d] += 1
out["职责TOP10"] = [{"职责": k, "命中": v, "占比%": pct(v)} for k, v in dc.most_common(10)]

# 薪资
sal = []
unparsed = 0
for r in rows:
    ps = S.parse_salary(r["salary"])
    if ps is None:
        unparsed += 1
    else:
        ps["cg"] = S.city_group(r["city"])
        ps["exp"] = S.norm_experience(r["experience"])
        ps["band"] = S.band_of(ps["mid_wan"])
        ps["kw"] = r["__kw"]
        ps["plat"] = r["platform"]
        sal.append(ps)
out["薪资"] = {"可解析": len(sal), "不可解析": unparsed}
for grp in ["成都组", "一线组"]:
    gr = [p for p in sal if p["cg"] == grp]
    bands = Counter(p["band"] for p in gr)
    g = {"样本": len(gr),
         "区间分布": {b: {"计数": bands.get(b, 0), "占比%": S.pct(bands.get(b, 0), len(gr))} for b in S.BAND_ORDER},
         "分经验段": {}}
    for eb in S.EXP_BUCKETS:
        sub = [p for p in gr if p["exp"] == eb]
        if sub:
            g["分经验段"][eb] = {"样本": len(sub),
                                "中位_万每月": round(statistics.median([p["mid_wan"] for p in sub]), 3)}
    out["薪资"][grp] = g

# 两关键词画像
for kw in ["AI应用开发", "Agent开发"]:
    kr = [r for r in rows if r["__kw"] == kw]
    kc = Counter()
    for r in kr:
        for s in S.skills_hit(r):
            kc[s] += 1
    ksal = [p for p in sal if p["kw"] == kw]
    out.setdefault("关键词画像", {})[kw] = {
        "样本": len(kr),
        "技能TOP10": [{"技能": k, "命中": v, "占比%": S.pct(v, len(kr))} for k, v in kc.most_common(10)],
        "薪资中位_万每月": round(statistics.median([p["mid_wan"] for p in ksal]), 3) if ksal else None,
        "薪资样本": len(ksal),
    }

# 平台差异
for plat in ["Boss直聘", "51job"]:
    pr = [r for r in rows if r["platform"] == plat]
    pn = len(pr)
    pcg = Counter(S.city_group(r["city"]) for r in pr)
    pedu = Counter(S.norm_education(r["education"]) for r in pr)
    psc = Counter()
    for r in pr:
        for s in S.skills_hit(r):
            psc[s] += 1
    psal = [p for p in sal if p["plat"] == plat]
    out.setdefault("平台", {})[plat] = {
        "样本": pn,
        "城市分组": {k: {"计数": v, "占比%": S.pct(v, pn)} for k, v in pcg.most_common()},
        "学历": {k: {"计数": pedu.get(k, 0), "占比%": S.pct(pedu.get(k, 0), pn)}
                for k in ["不限","大专","大专及以上","本科","硕士","博士","未标注","其他"] if pedu.get(k, 0)},
        "薪资中位_万每月": round(statistics.median([p["mid_wan"] for p in psal]), 3) if psal else None,
        "技能TOP12": [{"技能": k, "命中": v, "占比%": S.pct(v, pn)} for k, v in psc.most_common(12)],
    }

# 可投岗位筛选
appl = []
for r in rows:
    if S.norm_education(r["education"]) not in ("不限", "大专", "大专及以上"): continue
    if S.is_big_company(r["company"]): continue
    appl.append(r)
with open(os.path.join(ANA, "可投岗位清单_剔除全栈版_20261027.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["平台","关键词","岗位名称","公司","城市","薪资","经验","学历","技能标签"])
    for r in appl:
        w.writerow([r["platform"], r["__kw"], r["job_title"], r["company"], r["city"],
                    r["salary"], r["experience"], r["education"], r["skills"]])
ap_sal = []
for r in appl:
    ps = S.parse_salary(r["salary"])
    if ps: ap_sal.append(ps)
ap_cd = [r for r in appl if r["city"].startswith("成都")]
ap_cd_sal = []
for r in ap_cd:
    ps = S.parse_salary(r["salary"])
    if ps: ap_cd_sal.append(ps)
out["可投"] = {
    "总数": len(appl),
    "按平台": dict(Counter(r["platform"] for r in appl)),
    "按关键词": dict(Counter(r["__kw"] for r in appl)),
    "成都条数": len(ap_cd),
    "薪资中位_万每月": round(statistics.median([p["mid_wan"] for p in ap_sal]), 3) if ap_sal else None,
    "成都薪资中位_万每月": round(statistics.median([p["mid_wan"] for p in ap_cd_sal]), 3) if ap_cd_sal else None,
}

with open(os.path.join(ANA, "stats_no_fullstack.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)

# 打印关键数字
print("样本:", n, out["文件"])
print("技能TOP5:", [(x["技能"], x["占比%"]) for x in out["技能TOP20"][:5]])
print("成都分经验:", out["薪资"]["成都组"]["分经验段"])
print("一线分经验:", out["薪资"]["一线组"]["分经验段"])
print("可投:", out["可投"])
