# 跨境电商AI全链路助手 (Cross-border E-commerce AI Copilot)

> 用AI打通跨境电商「选品 → 图文 → 视频 → 运营」全流程

## 项目简介

面向跨境电商卖家的AI全链路助手，覆盖从选品调研到上架运营的完整工作流：

- **选品**：卖家精灵数据接入 + 竞品分析 + 评论挖掘 + RAG选品知识库
- **图文**：Listing文案生成 + 产品图生成（通义万相API + ComfyUI）+ 合规审核
- **视频**：脚本生成 + AI视频（即梦Seedance）+ 配音 + 字幕 + 自动合成
- **运营**：评论情感分析 + 客服FAQ + 广告文案 + 数据看板

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.11 |
| LLM框架 | LangChain 0.2 + LangGraph 0.1 |
| 后端 | FastAPI 0.110 |
| 前端 | Streamlit 1.34 |
| 数据库 | PostgreSQL 16 + Chroma向量库 |
| 缓存/队列 | Redis 7 + Celery |
| 对象存储 | MinIO |
| 多模态 | DeepSeek / Qwen-VL / 通义万相 / 即梦Seedance / CosyVoice |
| 低代码 | Dify |
| 部署 | Docker + Docker Compose |
| 开发 | Cursor + GitHub Copilot |

## 快速开始

### 1. 环境要求
- Docker Desktop
- Python 3.11+
- Poetry（可选，用于本地开发）

### 2. 启动基础服务
```bash
cp .env.example .env
docker-compose up -d postgres redis minio chroma
```

### 3. 运行开发脚本
```bash
# 安装依赖
pip install -r requirements.txt

# 运行第一个脚本
python scripts/csv_stats.py
```

## 项目结构

```
E-commerce-ai/
├── app/                    # 主应用代码
│   ├── api/               # FastAPI路由
│   ├── agents/            # LangGraph Agent
│   ├── rag/               # RAG知识库
│   ├── services/          # 业务服务
│   └── core/              # 配置/工具
├── scripts/               # 工具脚本
├── data/                  # 数据文件
├── prompts/               # Prompt模板库
├── comfyui-workflows/     # ComfyUI工作流
├── docker/                # Docker配置
├── docs/                  # 文档
├── docker-compose.yml
├── .env.example
├── .cursorrules
└── README.md
```

## 开发进度

- [ ] Phase 1：选品 + RAG知识库（W1-6）
- [ ] Phase 2：图文生成（W7-12）
- [ ] Phase 3：视频生成（W13-18）
- [ ] Phase 4：运营 + 整合 + 部署（W19-24）

## 开发规范

- 每天至少1次commit，commit message遵循Conventional Commits规范
- Python代码遵循PEP 8，使用ruff格式化
- 配置通过环境变量管理，密钥不入库
- AI生成代码必须逐行review后才能commit
