"""N1 任务卡：CLI 多轮对话 v0.1

================================================================
预计工时：2.5h（不含装环境）    对应里程碑：M1
完成标志：连续聊 6 轮不断，逐字输出，每轮打印 4 个 token 数，三种退出方式都不报错
================================================================

【官方用法】
以下只写官方文档里存在的用法，不含任何业务实现。抄用法可以，别抄我写的结构。

----------------------------------------------------------------
1. OpenAI 客户端构造
来源：openai-python README / DeepSeek 官方文档「Your First API Call」
----------------------------------------------------------------
    from openai import OpenAI

    client = OpenAI(
        api_key=...,                 # 从环境变量取，不要写字面量
        base_url="https://api.deepseek.com",
        timeout=60.0,                # 秒；float 或 httpx.Timeout
        max_retries=0,               # SDK 内置重试次数，默认 2
    )

    官方参数名就是 api_key / base_url / timeout / max_retries 这四个。

----------------------------------------------------------------
2. 发起对话请求
来源：DeepSeek 官方 API 文档「Chat Completions API」
----------------------------------------------------------------
    resp = client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role": "system", "content": "..."},
                  {"role": "user",   "content": "..."}],
        stream=False,
    )

    关键参数（官方）：
      model        str   当前可选 deepseek-flash / deepseek-v4-pro
      messages     list[dict]  每项 {"role": "system|user|assistant", "content": str}
      stream       bool  默认 False
      stream_options  dict  仅 stream=True 时有效，可传 {"include_usage": True}

----------------------------------------------------------------
3. 非流式响应取值
来源：同上「Responses」章节
----------------------------------------------------------------
    resp.choices[0].message.content          # str，模型回答
    resp.usage.prompt_tokens                 # int
    resp.usage.completion_tokens             # int
    resp.usage.prompt_cache_hit_tokens       # int
    resp.usage.prompt_cache_miss_tokens      # int
    resp.usage.total_tokens                  # int

----------------------------------------------------------------
4. 流式响应结构
来源：同上「stream / stream_options」段落
----------------------------------------------------------------
    stream = client.chat.completions.create(..., stream=True,
                                            stream_options={"include_usage": True})
    for chunk in stream:
        chunk.choices[0].delta.content       # str | None，增量文本
        chunk.usage                          # 仅最后一个内容 chunk 上是 usage，前序为 None

    官方原文要点：不存在独立的 usage-only chunk，统计数字挂在最后一个内容 chunk 上，
    该 chunk 的 choices 仍有 1 个元素（不带新内容、finish_reason 非空）。

----------------------------------------------------------------
5. 需要用到时再查（Python 标准库）
来源：docs.python.org/3/library/os.html、/functions.html、/stdtypes.html
----------------------------------------------------------------
    os.environ["KEY"]            # 取环境变量，不存在抛 KeyError
    os.environ.get("KEY")        # 取不到返回 None
    input(prompt)                # 读一行，EOF 时抛 EOFError
    print(text, end="", flush=True)   # flush=True 立即冲刷缓冲区
    messages[-n:]                # 列表切片取末尾 n 个
    list(messages)               # 浅拷贝

================================================================
【需求清单】逐条做完打勾，每条都要能被观察到
================================================================

R1  客户端构造（build_client）
  R1.1  从环境变量 DEEPSEEK_API_KEY 读 key；代码里不出现任何明文 key
  R1.2  环境变量缺失时，打印一句人能看懂的话（例如"缺少 DEEPSEEK_API_KEY"）并退出，
        不要抛一屏 KeyError 栈
  R1.3  显式传 timeout=60.0
  R1.4  显式传 max_retries=0（重试后面自己控，先关掉 SDK 内置的）

R2  单次流式请求（chat_once）
  R2.1  请求时 stream=True，并传 stream_options={"include_usage": True}
  R2.2  遍历每个 chunk，取 choices[0].delta.content；为 None 时跳过，不要拼进结果
  R2.3  打印增量文本时必须 end="" 且 flush=True（否则看不到逐字）
  R2.4  遇到 chunk.usage 不为 None 时，把它记下来
  R2.5  返回 (完整回答字符串, usage 对象或 None)
  R2.6  不吞异常：网络错误、鉴权错误要能冒出来（后面任务 D 再统一处理重试）

R3  历史裁剪（trim_history）
  R3.1  system 消息永远保留，且永远在返回列表的 index 0
  R3.2  除 system 外只保留最近 max_turns 轮；1 轮 = 1 条 user + 1 条 assistant
  R3.3  返回新列表，不许原地修改入参
  R3.4  当轮数不足 max_turns，或 max_turns <= 0 时，返回 system + 全部历史（仍是新列表）
  R3.5  裁掉的必须是最早的轮次，不是最新的

R4  交互主循环（main）
  R4.1  循环读一行输入，strip 后为空则跳过本轮
  R4.2  输入 exit / quit / q 时打印告别语并正常结束
  R4.3  Ctrl+C（KeyboardInterrupt）和 EOF（EOFError）都能优雅退出，不抛 traceback
  R4.4  输入 /context 时打印当前 messages 的条数，然后继续循环
  R4.5  一轮正常对话的顺序：追加 user 消息 → 裁历史 → 调 chat_once → 追加 assistant 消息
  R4.6  每轮结束打印 in / out / cache_hit / cache_miss 四个数；
        usage 为 None 时打印一行提示，不许崩

================================================================
【验收】跑起来逐条对照
================================================================
  [ ] 连聊 6 轮后输入 /context 显示 13（1 条 system + 6 轮 x 2）；第 7 轮起总数不再涨
  [ ] 回答是逐字出现的，不是停顿几秒后整段弹出
  [ ] 每轮都打印 in / out / cache_hit / cache_miss
  [ ] exit、/q、Ctrl+C 三种退出都不抛 traceback
  [ ] 故意把 key 改错跑一次，看到的是清晰的一句话，不是一屏栈

【卡点】只给方向，不给修法
  - 聊两三轮后模型开始答非所问 → 想想 system 那一项是不是被一起裁掉了
  - 看不到逐字，卡几秒才整段弹出 → 看 print 的两个参数
  - AttributeError: 'NoneType' object has no attribute 'prompt_tokens' → usage 不一定有值
  - 第 7 轮 /context 还在涨 → 裁剪的时机错了，或者只裁了 user 没裁 assistant
  - 语法没错但一直没输出 → 可能卡在流式迭代里，先确认请求本身通了（用非流式试一次）
================================================================
"""
import os

from openai import OpenAI

MODEL = "deepseek-flash"
BASE_URL = "https://api.deepseek.com"
SYSTEM_PROMPT = "你是一个跨境电商选品助手，回答简洁；不确定就直说不知道。"
MAX_HISTORY_TURNS = 6


def build_client() -> OpenAI:
    """按 R1.1 - R1.4 构造客户端。"""
    raise NotImplementedError("R1.1 / R1.2 / R1.3 / R1.4")


def trim_history(messages: list[dict], max_turns: int) -> list[dict]:
    """按 R3.1 - R3.5 裁剪历史，返回新列表。"""
    raise NotImplementedError("R3.1 / R3.2 / R3.3 / R3.4 / R3.5")


def chat_once(client: OpenAI, messages: list[dict]) -> tuple[str, object | None]:
    """按 R2.1 - R2.6 发起一次流式请求。"""
    raise NotImplementedError("R2.1 / R2.2 / R2.3 / R2.4 / R2.5 / R2.6")


def main() -> None:
    """按 R4.1 - R4.6 实现交互循环。"""
    raise NotImplementedError("R4.1 / R4.2 / R4.3 / R4.4 / R4.5 / R4.6")


if __name__ == "__main__":
    main()
