# -*- coding: utf-8 -*-
"""
剔除全栈版统计（2026-10-29采集，4文件435条纯AI岗位）
自包含：技能词典/薪资解析/经验分桶/平台差异/可投筛选，全部数字实算。
"""
import csv, json, os, re, statistics
from collections import Counter

BASE = r"E:\ai-project\E-commerce-ai\documents\job-research-2026-10"
DATA = os.path.join(BASE, "data")
ANA = os.path.join(BASE, "analysis")

FILES = [
    "boss_ai_dev_20261029.csv",
    "boss_agent_dev_20261029.csv",
    "51job_ai_dev_20261029.csv",
    "51job_agent_dev_20261029.csv",
]

BIG = ["华为","字节","腾讯","阿里","美团","百度","京东","网易","小米","中兴","OPPO","oppo",
       "vivo","拼多多","快手","大疆","立讯","药明","赛力斯","黑芝麻","科大讯飞","滴滴",
       "哔哩哔哩","蚂蚁","商汤","阿里云","字节跳动"]

# ---------------- 技能词典 ----------------
SKILL_DICT = [
    ("Python",      {"tokens": ["python"], "subs": ["python"]}),
    ("Java",         {"tokens": ["java"], "subs": []}),
    ("Go/Golang",    {"tokens": ["go", "golang"], "subs": []}),
    ("C++/C",        {"tokens": ["c++", "c", "c#"], "subs": []}),
    ("JavaScript",   {"tokens": ["javascript", "js"], "subs": []}),
    ("TypeScript",   {"tokens": ["typescript", "ts"], "subs": []}),
    ("Vue",          {"tokens": ["vue"], "subs": []}),
    ("React",        {"tokens": ["react", "react.js"], "subs": []}),
    ("Node.js",      {"tokens": ["node.js", "nodejs", "node"], "subs": []}),
    ("SpringBoot",   {"tokens": ["spring", "springboot", "spring boot", "springmvc"], "subs": []}),
    ("MySQL/PostgreSQL", {"tokens": ["mysql", "postgresql", "postgre", "pg", "oracle", "sqlserver", "mybatis"], "subs": []}),
    ("SQL",          {"tokens": ["sql"], "subs": []}),
    ("Redis",        {"tokens": ["redis"], "subs": []}),
    ("MongoDB",      {"tokens": ["mongodb", "mongo"], "subs": []}),
    ("Elasticsearch", {"tokens": ["elasticsearch", "es"], "subs": []}),
    ("LangChain",    {"tokens": ["langchain"], "subs": ["langchain"]}),
    ("LangGraph",    {"tokens": ["langgraph"], "subs": ["langgraph"]}),
    ("LlamaIndex",   {"tokens": ["llamaindex", "llama_index"], "subs": []}),
    ("Dify",         {"tokens": ["dify"], "subs": ["dify"]}),
    ("Coze",         {"tokens": ["coze"], "subs": ["coze"]}),
    ("AutoGen/CrewAI", {"tokens": ["autogen", "crewai", "crew"], "subs": ["autogen", "crewai"]}),
    ("RAG",          {"tokens": ["rag"], "subs": ["rag", "检索增强"]}),
    ("向量数据库",    {"tokens": ["milvus", "faiss", "chroma", "qdrant", "pinecone", "向量数据库", "向量库", "向量入库", "向量"], "subs": ["向量数据库", "向量库", "向量入库", "向量化"]}),
    ("Milvus",       {"tokens": ["milvus"], "subs": []}),
    ("FAISS",        {"tokens": ["faiss"], "subs": []}),
    ("Chroma",       {"tokens": ["chroma"], "subs": []}),
    ("Qdrant",       {"tokens": ["qdrant"], "subs": []}),
    ("Pinecone",     {"tokens": ["pinecone"], "subs": []}),
    ("知识图谱",      {"tokens": [], "subs": ["知识图谱"]}),
    ("Prompt工程",    {"tokens": ["prompt"], "subs": ["prompt", "提示词"]}),
    ("Function Call/工具调用", {"tokens": ["function call", "function calling", "tool call", "tool calling", "functioncall", "toolcall", "functioncalls", "toolcalls"], "subs": ["function call", "tool call", "工具调用", "函数调用"]}),
    ("Multi-Agent/多智能体", {"tokens": ["multi-agent", "multiagent", "multi agent"], "subs": ["多智能体", "multi-agent", "multiagent"]}),
    ("Agent/智能体",  {"tokens": ["agent", "ai agent", "智能体"], "subs": ["agent", "智能体"]}),
    ("记忆/Memory",   {"tokens": [], "subs": ["记忆", "memory", "上下文管理"]}),
    ("Workflow/工作流", {"tokens": ["workflow", "n8n"], "subs": ["工作流", "workflow"]}),
    ("MCP协议",       {"tokens": [], "subs": ["mcp"]}),
    ("大模型API/LLM", {"tokens": ["llm"], "subs": ["大模型", "llm", "aigc", "生成式ai"]}),
    ("DeepSeek",      {"tokens": ["deepseek"], "subs": ["deepseek"]}),
    ("OpenAI",        {"tokens": ["openai"], "subs": ["openai"]}),
    ("Qwen/通义",     {"tokens": ["qwen", "通义"], "subs": ["通义", "qwen", "千问"]}),
    ("Claude",        {"tokens": ["claude"], "subs": ["claude"]}),
    ("模型微调/LoRA", {"tokens": ["lora", "qlora", "sft", "dpo"], "subs": ["微调", "lora", "qlora", "finetune", "fine-tuning", "sft", "dpo"]}),
    ("PyTorch",       {"tokens": ["pytorch"], "subs": ["pytorch"]}),
    ("TensorFlow",    {"tokens": ["tensorflow"], "subs": ["tensorflow"]}),
    ("vLLM/Ollama",   {"tokens": ["vllm", "ollama", "sglang"], "subs": ["vllm", "ollama"]}),
    ("机器学习/深度学习", {"tokens": ["机器学习", "深度学习", "ml", "dl"], "subs": ["机器学习", "深度学习"]}),
    ("Docker/容器",   {"tokens": ["docker"], "subs": ["docker", "容器化"]}),
    ("K8s/容器编排",  {"tokens": ["k8s", "kubernetes"], "subs": ["k8s", "kubernetes"]}),
    ("Linux",         {"tokens": ["linux"], "subs": ["linux"]}),
    ("Git",           {"tokens": ["git"], "subs": ["git", "版本管理", "版本控制"]}),
    ("CI/CD",         {"tokens": [], "subs": ["ci/cd", "持续集成", "持续部署"]}),
    ("FastAPI",       {"tokens": ["fastapi"], "subs": ["fastapi"]}),
    ("Flask",         {"tokens": ["flask"], "subs": ["flask"]}),
    ("WebSocket",     {"tokens": ["websocket"], "subs": ["websocket", "web socket"]}),
    ("Streamlit",     {"tokens": ["streamlit"], "subs": ["streamlit"]}),
    ("Gradio",        {"tokens": ["gradio"], "subs": ["gradio"]}),
    ("后端/API开发",   {"tokens": ["api", "后端", "后端开发"], "subs": ["后端", "接口开发", "api接口", "系统集成"]}),
    ("全栈",          {"tokens": ["全栈"], "subs": ["全栈"]}),
    ("前端",          {"tokens": ["前端", "web前端", "web前端开发"], "subs": ["前端"]}),
    ("分布式/高并发",  {"tokens": [], "subs": ["分布式", "高并发", "微服务"]}),
    ("低代码平台",     {"tokens": [], "subs": ["低代码"]}),
    ("FDE/前沿部署",   {"tokens": ["fde"], "subs": ["fde", "前沿部署", "前线部署"]}),
    ("售前/客户交付",  {"tokens": [], "subs": ["售前", "客户培训", "解决方案", "需求调研", "客户交付"]}),
    ("测试/评测",      {"tokens": [], "subs": ["测试", "评测", "质量保障", "qa", "单元测试"]}),
    ("OCR/多模态",     {"tokens": ["ocr"], "subs": ["ocr", "asr", "tts", "多模态", "语音识别"]}),
]

DUTY_RULES = [
    ("LLM应用开发与落地",      ["大模型", "llm", "aigc", "生成式ai", "ai应用", "应用落地", "应用开发", "模型落地"]),
    ("Agent开发与工作流编排",   ["agent", "智能体", "工作流", "workflow", "任务拆解", "langgraph", "crewai"]),
    ("RAG知识库搭建与优化",     ["rag", "向量", "milvus", "faiss", "chroma", "qdrant", "pinecone", "知识图谱", "知识库", "检索"]),
    ("Prompt工程与效果优化",   ["prompt", "提示词", "调优", "效果优化"]),
    ("模型微调与训练",         ["lora", "qlora", "微调", "finetune", "pytorch", "tensorflow", "模型训练", "sft"]),
    ("后端API开发与服务封装",   ["api", "fastapi", "flask", "spring", "node", "后端", "mysql", "redis", "websocket", "接口", "系统集成"]),
    ("部署运维与工程化",       ["docker", "linux", "k8s", "容器", "运维", "nginx", "部署"]),
    ("大模型API对接与集成",     ["openai", "deepseek", "qwen", "通义", "claude", "llm api"]),
    ("前端/全栈开发",          ["react", "vue", "javascript", "typescript", "node", "前端", "全栈"]),
    ("业务需求对接与客户交付",  ["需求调研", "售前", "客户培训", "解决方案", "fde", "交付", "客户", "业务"]),
    ("多智能体架构设计",        ["multi-agent", "multiagent", "多智能体"]),
    ("测试与评测",             ["测试", "评测", "质量保障", "单元测试"]),
]

EXP_BUCKETS = ["经验不限/应届", "1-3年", "3-5年", "5-10年", "10年以上"]
BAND_ORDER = ["<8K", "8-12K", "12-15K", "15-20K", "20-30K", "30K+"]

# ---------------- 解析函数 ----------------
def parse_salary(text):
    if not text: return None
    s = str(text).strip()
    if ("面议" in s) or ("未公开" in s): return None
    # 日薪：220-320元/天 -> 按月21.75工作日折算
    m = re.match(r"([\d.]+)\s*-\s*([\d.]+)\s*元/天", s)
    if m:
        lw, hw = float(m.group(1)), float(m.group(2))
        return {"low_wan": round(lw*21.75/10000, 4), "high_wan": round(hw*21.75/10000, 4),
                "mid_wan": round((lw+hw)/2*21.75/10000, 4), "days": True}
    months = 12
    m = re.search(r"·(\d+)\s*薪", s)
    if m: months = int(m.group(1))
    annual = ("万/年" in s) or ("万年" in s)
    body = re.sub(r"·\d+\s*薪", "", s)
    parts = re.split(r"[-—–]", body)
    if len(parts) != 2: return None
    def to_wan(x):
        x = x.strip()
        mm = re.match(r"([\d.]+)\s*(万|千)?", x)
        if not mm: return None
        v = float(mm.group(1)); u = mm.group(2)
        return v/10.0 if u == "千" else (v if u == "万" else v/10.0)
    lw, hw = to_wan(parts[0]), to_wan(parts[1])
    if lw is None or hw is None or lw <= 0 or hw <= 0: return None
    if annual: lw, hw = lw/12.0, hw/12.0
    if lw > hw: lw, hw = hw, lw
    return {"low_wan": round(lw,4), "high_wan": round(hw,4), "mid_wan": round((lw+hw)/2,4), "months": months, "annual": annual}

def _lower_bucket(n):
    if n <= 2: return "1-3年"
    if n in (3,4): return "3-5年"
    if n in (5,6,7,8,9): return "5-10年"
    return "10年以上"

def norm_experience(text):
    s = str(text).strip()
    if ("无需经验" in s) or ("不限" in s) or ("应届" in s) or ("天/周" in s):
        return "经验不限/应届"
    m = re.match(r"(\d+)\s*[-—–]\s*(\d+)\s*年", s)
    if m:
        mid = (int(m.group(1))+int(m.group(2)))/2.0
        if mid < 2.5: return "1-3年"
        if mid < 4.5: return "3-5年"
        if mid < 9: return "5-10年"
        return "10年以上"
    m = re.match(r"(\d+)\s*年及以上", s)
    if m: return _lower_bucket(int(m.group(1)))
    m = re.match(r"(\d+)\s*年$", s)
    if m: return _lower_bucket(int(m.group(1)))
    return "其他"

EDU_ORDER = ["不限","大专","大专及以上","本科","统招本科","硕士","博士","未标注","其他"]
def norm_education(text):
    s = str(text).strip()
    if not s: return "未标注"
    if s in ("学历不限","不限"): return "不限"
    if "大专及以上" in s: return "大专及以上"
    if s in EDU_ORDER: return s
    return "其他"

def city_group(city):
    c = str(city)
    if c.startswith("成都"): return "成都组"
    if any(x in c for x in ["北京","上海","深圳","广州","杭州"]): return "一线组"
    return "其他组"

def is_big(name): return any(b in str(name) for b in BIG)

def pct(x, total): return round(100.0*x/total, 1) if total else 0.0

def skills_hit(row):
    tokens = set(t.strip().lower() for t in re.split(r"[,，;；|]", str(row.get("skills",""))) if t.strip())
    text = " ".join([str(row.get("job_title","")), str(row.get("skills","")), str(row.get("duty_summary",""))]).lower()
    hits = []
    for name, rule in SKILL_DICT:
        ok = any(t in tokens for t in rule.get("tokens",[]))
        if not ok: ok = any(s in text for s in rule.get("subs",[]) if s)
        if ok: hits.append(name)
    return hits

def duty_hit(row):
    text = " ".join([str(row.get("job_title","")), str(row.get("skills","")), str(row.get("duty_summary",""))]).lower()
    return [name for name, kws in DUTY_RULES if any(k in text for k in kws)]

def band_of(m):
    k = m*10
    if k < 8: return "<8K"
    if k < 12: return "8-12K"
    if k < 15: return "12-15K"
    if k < 20: return "15-20K"
    if k < 30: return "20-30K"
    return "30K+"

# ---------------- 加载 ----------------
rows = []
for fn in FILES:
    with open(os.path.join(DATA, fn), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if not r.get("job_title"): continue
            r["__file"] = fn
            r["platform"] = r["platform"].strip()
            r["__kw"] = "AI应用开发" if "ai_dev" in fn else "Agent开发"
            rows.append(r)
n = len(rows)
out = {"样本量": n, "文件": {fn: sum(1 for r in rows if r["__file"]==fn) for fn in FILES}}

cg = Counter(city_group(r["city"]) for r in rows)
out["城市分组"] = {k:{"计数":v,"占比%":pct(v,n)} for k,v in cg.most_common()}

edu = Counter(norm_education(r["education"]) for r in rows)
out["学历分布"] = {k:{"计数":edu.get(k,0),"占比%":pct(edu.get(k,0),n)} for k in EDU_ORDER if edu.get(k,0)}

exp = Counter(norm_experience(r["experience"]) for r in rows)
out["经验分布"] = {k:{"计数":exp.get(k,0),"占比%":pct(exp.get(k,0),n)} for k in EXP_BUCKETS+["其他"] if exp.get(k,0)}

sc = Counter()
for r in rows:
    for s in skills_hit(r): sc[s] += 1
out["技能TOP20"] = [{"技能":k,"命中":v,"占比%":pct(v,n)} for k,v in sc.most_common(20)]

dc = Counter()
for r in rows:
    for d in duty_hit(r): dc[d] += 1
out["职责TOP10"] = [{"职责":k,"命中":v,"占比%":pct(v,n)} for k,v in dc.most_common(10)]

sal = []; unparsed = 0
for r in rows:
    ps = parse_salary(r["salary"])
    if ps is None: unparsed += 1
    else:
        ps["cg"] = city_group(r["city"]); ps["exp"] = norm_experience(r["experience"])
        ps["band"] = band_of(ps["mid_wan"]); ps["kw"] = r["__kw"]; ps["plat"] = r["platform"]
        sal.append(ps)
out["薪资"] = {"可解析": len(sal), "不可解析": unparsed}
for grp in ["成都组","一线组"]:
    gr = [p for p in sal if p["cg"]==grp]
    bands = Counter(p["band"] for p in gr)
    g = {"样本":len(gr),
         "区间分布":{b:{"计数":bands.get(b,0),"占比%":pct(bands.get(b,0),len(gr))} for b in BAND_ORDER},
         "分经验段":{}}
    for eb in EXP_BUCKETS:
        sub = [p for p in gr if p["exp"]==eb]
        if sub:
            g["分经验段"][eb] = {"样本":len(sub), "中位_万每月":round(statistics.median([p["mid_wan"] for p in sub]),3)}
    out["薪资"][grp] = g

for kw in ["AI应用开发","Agent开发"]:
    kr = [r for r in rows if r["__kw"]==kw]
    kc = Counter()
    for r in kr:
        for s in skills_hit(r): kc[s] += 1
    ksal = [p for p in sal if p["kw"]==kw]
    out.setdefault("关键词画像",{})[kw] = {
        "样本":len(kr),
        "技能TOP10":[{"技能":k,"命中":v,"占比%":pct(v,len(kr))} for k,v in kc.most_common(10)],
        "薪资中位_万每月":round(statistics.median([p["mid_wan"] for p in ksal]),3) if ksal else None,
        "薪资样本":len(ksal)}

for plat in ["Boss直聘","51job"]:
    pr = [r for r in rows if r["platform"]==plat]; pn = len(pr)
    pcg = Counter(city_group(r["city"]) for r in pr)
    pedu = Counter(norm_education(r["education"]) for r in pr)
    psc = Counter()
    for r in pr:
        for s in skills_hit(r): psc[s] += 1
    psal = [p for p in sal if p["plat"]==plat]
    out.setdefault("平台",{})[plat] = {
        "样本":pn,
        "城市分组":{k:{"计数":v,"占比%":pct(v,pn)} for k,v in pcg.most_common()},
        "学历":{k:{"计数":pedu.get(k,0),"占比%":pct(pedu.get(k,0),pn)} for k in EDU_ORDER if pedu.get(k,0)},
        "薪资中位_万每月":round(statistics.median([p["mid_wan"] for p in psal]),3) if psal else None,
        "技能TOP12":[{"技能":k,"命中":v,"占比%":pct(v,pn)} for k,v in psc.most_common(12)]}

appl = [r for r in rows if norm_education(r["education"]) in ("不限","大专","大专及以上") and not is_big(r["company"])]
with open(os.path.join(ANA,"可投岗位清单_剔除全栈版_20261029.csv"),"w",encoding="utf-8-sig",newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["平台","关键词","岗位名称","公司","城市","薪资","经验","学历","技能标签"])
    for r in appl:
        w.writerow([r["platform"],r["__kw"],r["job_title"],r["company"],r["city"],r["salary"],r["experience"],r["education"],r["skills"]])
ap_sal = [parse_salary(r["salary"]) for r in appl if parse_salary(r["salary"])]
ap_cd = [r for r in appl if r["city"].startswith("成都")]
ap_cd_sal = [parse_salary(r["salary"]) for r in ap_cd if parse_salary(r["salary"])]
out["可投"] = {
    "总数":len(appl),
    "按平台":dict(Counter(r["platform"] for r in appl)),
    "按关键词":dict(Counter(r["__kw"] for r in appl)),
    "成都条数":len(ap_cd),
    "薪资中位_万每月":round(statistics.median([p["mid_wan"] for p in ap_sal]),3) if ap_sal else None,
    "成都薪资中位_万每月":round(statistics.median([p["mid_wan"] for p in ap_cd_sal]),3) if ap_cd_sal else None}

with open(os.path.join(ANA,"stats_no_fullstack_029.json"),"w",encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)

print("样本:", n, out["文件"])
print("城市:", out["城市分组"])
print("学历:", out["学历分布"])
print("经验:", out["经验分布"])
print("技能TOP10:", [(x["技能"],x["占比%"]) for x in out["技能TOP20"][:10]])
print("成都分经验:", out["薪资"]["成都组"]["分经验段"])
print("一线分经验:", out["薪资"]["一线组"]["分经验段"])
print("成都区间:", out["薪资"]["成都组"]["区间分布"])
print("一线区间:", out["薪资"]["一线组"]["区间分布"])
print("关键词:", {k:{"样本":v["样本"],"中位":v["薪资中位_万每月"]} for k,v in out["关键词画像"].items()})
print("平台:", {k:{"样本":v["样本"],"中位":v["薪资中位_万每月"],"学历":v["学历"]} for k,v in out["平台"].items()})
print("可投:", out["可投"])
