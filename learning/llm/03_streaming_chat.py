# ============================================
# 03 流式输出 —— 像ChatGPT一样逐字蹦出来
# 学习日期：9.24 周四（3h）
# ============================================

# 【学习目标】
# 1. 理解 stream=True 的作用
# 2. 用 for 循环逐块接收AI回复
# 3. 对比非流式 vs 流式的体验差异

# 【核心概念】
# 非流式：AI在后台把整段话写完 → 一次性返回给你 → 你干等5秒
# 流式：  AI写一个字就发一个字 → 你立刻看到 → 感知响应时间从5秒降到0.5秒

# ========== 初始化 ==========
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

messages = [
    {"role": "system", "content": "你是跨境电商选品顾问，回答要简洁"},
]

print("=== 流式输出演示（输入'退出'结束）===\n")

# ========== 你的任务 ==========

# 照着02_multi_chat.py的结构，写一个while循环持续对话。
# 区别：这次调用API时加 stream=True，然后逐块接收。
#
# 你需要做的：
#   1. while True循环，input获取用户输入
#   2. 输入"退出"就break
#   3. 用户消息append到messages
#   4. 调 create() 时加 stream=True
#   5. 返回的是一个流（生成器），用 for chunk in stream 遍历
#   6. 每个chunk的文字在 chunk.choices[0].delta.content（可能是None）
#   7. 边收边打印（print加 end="", flush=True）
#   8. 把完整回复拼起来，存到messages

# ========== 测试 ==========
# 1. 问"详细分析一下宠物用品类目的选品思路"，看是不是逐字出的
# 2. 和02对比：非流式 vs 流式的体验差异
# 3. 连续聊3轮看上下文是否正常

# ============================================
# 【验收标准】
# ✅ AI回复是逐字蹦出来的
# ✅ 连续聊3轮不丢上下文
# ✅ 能说清楚 stream=True 和不加的区别
# ============================================
