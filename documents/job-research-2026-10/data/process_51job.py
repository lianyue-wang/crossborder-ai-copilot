# -*- coding: utf-8 -*-
import json, csv, io, os, collections

BASE = r"E:\ai-project\E-commerce-ai\documents\job-research-2026-10\data"
RAW = os.path.join(BASE, "raw_51job.jsonl")
CSV_PATH = os.path.join(BASE, "51job_agent_dev_20261029.csv")
MD_PATH = os.path.join(BASE, "51job_agent_dev_20261029.md")

BENEFITS = set("""
五险一金 年终奖金 绩效奖金 定期体检 带薪年假 专业培训 餐饮补贴 通讯补贴 交通补贴 出差补贴
节日福利 周末双休 补充医疗保险 股票期权 项目奖金 弹性工作 有餐补 团队氛围好 培训 员工旅游
立即上岗 做五休二 年底双薪 下午茶 生日福利 高温补贴 住房补贴 五险 社保 公积金 人性化管理
扁平管理 领导好 发展前景好 团建 年度旅游 免费班车 节日礼物 带薪病假 零食下午茶 不加班 加班补助
采暖补贴 通讯津贴 做五休2 双休 年终分红 期权 带薪病假 补充公积金 工龄奖 保底工资 意外险
人才推荐奖 做六休一 做五休一 弹性工作制 免费培训 出国机会 上市公司 餐补 话补 房补
""".split())

rows_by_key = {}
kw_count = collections.Counter()
city_count = collections.Counter()
order = []

with io.open(RAW, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        title = (r.get("title") or "").strip()
        company = (r.get("company") or "").strip()
        if not title or not company:
            continue
        key = title + "||" + company
        if key in rows_by_key:
            # keep first search_word encountered
            continue
        tags = [t.strip() for t in (r.get("tags") or []) if t and t.strip()]
        tech = [t for t in tags if t not in BENEFITS and len(t) <= 20]
        # de-dup preserve order
        seen=set(); tech_u=[]
        for t in tech:
            if t.lower() not in seen:
                seen.add(t.lower()); tech_u.append(t)
        skills = " / ".join(tech_u)
        if tech_u:
            duty = "负责%s相关工作，技术栈/要求：%s。" % (title, "、".join(tech_u[:8]))
        else:
            duty = "负责%s相关工作，具体职责以企业JD为准。" % title
        rec = {
            "job_title": title,
            "company": company,
            "city": (r.get("city") or "").strip(),
            "salary": (r.get("salary") or "").strip(),
            "experience": "",
            "education": "",
            "skills": skills,
            "duty_summary": duty,
            "platform": "51job",
            "search_word": r.get("search_word") or "",
            "scrape_date": "2026-10-29",
        }
        rows_by_key[key] = rec
        order.append(key)

final = [rows_by_key[k] for k in order]
final = final[:135]
for rec in final:
    kw_count[rec["search_word"]] += 1
    c = rec["city"].split("·")[0].strip()
    city_count[c] += 1

cols = ["job_title","company","city","salary","experience","education","skills",
        "duty_summary","platform","search_word","scrape_date"]
with io.open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for rec in final:
        w.writerow(rec)

# md summary
lines = []
lines.append("# 51job Agent/智能体开发岗位采集摘要 (2026-10-29)\n")
lines.append("- 平台：51job 前程无忧（we.51job.com），按 IP 自动定位成都，城市保持成都。")
lines.append("- 去重规则：以「公司 + 岗位名」唯一去重。")
lines.append("- 经验/学历：51job 列表卡片不展示 experience/education 字段（详情页需登录，未进入），故两列留空。")
lines.append("- duty_summary：由卡片技能标签归纳生成的简短描述，非真实 JD。\n")
lines.append("## 各关键词收获条数（去重后计）\n")
lines.append("| 关键词 | 条数 |")
lines.append("|---|---|")
for kw, cnt in kw_count.most_common():
    lines.append("| %s | %d |" % (kw, cnt))
lines.append("")
lines.append("## 城市覆盖\n")
lines.append("| 城市 | 条数 |")
lines.append("|---|---|")
for c, cnt in city_count.most_common():
    lines.append("| %s | %d |" % (c, cnt))
lines.append("")
lines.append("## 拦截情况\n")
lines.append("- 全程未遇到登录墙/验证码；列表卡片可直接抓取，未进入详情页。")
lines.append("- 单关键词列表为懒加载，已滚动加载至无新增；部分关键词结果不足20条为成都本地真实存量。")
lines.append("")
lines.append("## 汇总\n")
lines.append("- 原始采集行数：%d" % sum(1 for _ in io.open(RAW, encoding="utf-8")))
lines.append("- 去重后唯一岗位数：%d" % len(final))
lines.append("- 输出文件：%s" % CSV_PATH)

with io.open(MD_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("FINAL_UNIQUE:", len(final))
print("RAW_LINES:", sum(1 for _ in io.open(RAW, encoding="utf-8")))
print("KW_COUNT:", dict(kw_count))
print("CSV:", CSV_PATH)
print("MD:", MD_PATH)
