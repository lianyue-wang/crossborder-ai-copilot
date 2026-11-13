# CLI 聊天机器人 v0.1（N1 交付物）

## 这是什么

最小可用的多轮对话 CLI：流式输出 + 历史裁剪 + Token 可观测。

**为什么先做它，而不是直接上 FastAPI**：后面所有模块（选品 Agent、Listing 生成、视频流水线）本质都是"拿 messages 调一次 LLM 再处理结果"，区别只是入口从 `input()` 换成 HTTP。这个 CLI 是后面全部代码的地基。地基里有三个坑（历史膨胀、流式 usage 位置、超时缺失），在这里踩一次十分钟；等它藏进 FastAPI + Celery 里再踩，两天。

## 怎么跑

```bash
# 1. 装依赖（先查当前版本，锁进 requirements.txt）
pip index versions openai
pip install "openai==<上面查到的版本>"

# 2. 配 key（Git Bash）
export DEEPSEEK_API_KEY=sk-xxxx
# PowerShell: $env:DEEPSEEK_API_KEY="sk-xxxx"

# 3. 跑
python cli/chat.py
```

## 需求在哪

全在 `chat.py` 的模块 docstring 里：先【官方用法】（5 段，都是官方文档里能查到的），再【需求清单】R1.1 – R4.6，逐条编号，每条都写了"完成标志"。

四个函数体都是 `raise NotImplementedError`，你自己写：

| 函数 | 需求编号 | 练的是什么 |
|---|---|---|
| `build_client` | R1.1 – R1.4 | 配置管理：凭据不进代码、超时必须显式给、关掉 SDK 隐式重试 |
| `chat_once` | R2.1 – R2.6 | 流式消费 + 可观测：生成器怎么吃、usage 从哪拿 |
| `trim_history` | R3.1 – R3.5 | 上下文工程：上下文是有成本的，不能无脑追加 |
| `main` | R4.1 – R4.6 | 交互循环与退出路径：三种退出都要干净 |

建议顺序：`build_client` → 先用**非流式**调通一次（验证 key 和网络）→ `chat_once` 改流式 → `trim_history` → 最后 `main` 把四个接起来。

## 验收（勾完才进下一步）

- [ ] 连聊 6 轮后 `/context` 显示 **13**（1 条 system + 6 轮 × 2）；第 7 轮起不再增长
- [ ] 回答**逐字**出现，不是停顿后整段弹出
- [ ] 每轮都打印 in / out / cache_hit / cache_miss
- [ ] `exit`、`/q`、Ctrl+C 三种退出都不抛 traceback
- [ ] 故意把 key 改错跑一次，看到的是清晰一句话，不是一屏栈

## 常见卡点（只给方向）

1. **聊两三后模型开始答非所问** → 想一下 `trim_history` 是不是把 system 那一项也一起裁掉了。
2. **看不到逐字，卡几秒才整段弹出** → 看 `print` 的参数，问题在缓冲。
3. **`AttributeError: 'NoneType' object has no attribute 'prompt_tokens'`** → usage 不一定有值，想想它在什么情况下会是 None。
4. **第 7 轮 `/context` 还在涨** → 裁剪时机错了，或者一轮只裁了一半。
5. **语法没错但一直没输出** → 先用非流式确认请求本身通了，再回来查流式迭代。

## 下一步（做完这个才开）

1. 任务 C：装饰器 `@track_cost` —— 自动记录每次调用耗时 + token + 折算成钱（正好用上你 W1 学的装饰器）
2. 任务 D：异常分类 + 三次指数退避重试 + Docker 打包
3. 任务 E：Pydantic 给消息结构做校验（为后面 Function Calling 的参数校验铺路）
