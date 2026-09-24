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
while True:
   userinput= input("你：")
   if userinput== "退出":
      break
   messages.append({"role":"user","content":userinput})
   model="deepseek-chat"
   response_stream=client.chat.completions.create(model=model, messages=messages,stream=True)
for response in response_stream():
  is_none= response. chunk.choices[0].delta.content
  if is_none==None:
     break
  print(f"AI流式输出 {is_none}",end="",flush=True)
  messages.append({"role":"system","content":is_none})

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
# ==================== 本文件需求的伪代码实现 ====================
# 前提：已完成初始化（client、messages列表）
# 1. 开启无限循环（实现持续多轮对话）
# while True:
#   1.1 获取用户输入 → user_input
#   1.2 若 user_input == "退出" → break（结束对话）
#   1.3 封装用户消息：{"role": "user", "content": user_input} → 追加到 messages
#   1.4 调用AI接口：传入 messages + stream=True → 得到【流式响应流】（不是一次性完整响应）
#   1.5 初始化完整AI回复变量 → full_ai_reply = ""
#   1.6 打印提示前缀（如"AI回复："）→ 让用户知道AI正在生成
#   1.7 遍历响应流的每个分块 chunk:
#     1.7.1 提取当前分块的文字内容 → delta_content = chunk.choices[0].delta.content
#     1.7.2 若 delta_content 不为 None → 执行两件事：
#           a. 打印 delta_content，设置 end=""（不换行） + flush=True（立即刷到终端，实现逐字显示）
#           b. 把 delta_content 拼接到 full_ai_reply
#   1.8 遍历完所有 chunk 后 → 封装AI完整回复：{"role": "assistant", "content": full_ai_reply} → 追加到 messages
#   1.9 打印换行 → 让下一轮用户输入位置更清晰

# ==================== 伪代码的原因说明 ====================
# 1. 用while True循环：满足【持续多轮对话】需求，是Python实现无限循环的标准写法，通过break控制退出
# 2. 输入"退出"就break：符合需求明确的【退出条件】，break能立即终止当前循环退出程序
# 3. 追加用户消息到messages：和02_non_stream的多轮对话逻辑统一，让AI能读取历史上下文（比如之前聊的选品思路）
# 4. 调用接口加stream=True：这是【流式输出】的核心开关——OpenAI兼容API会返回【生成器对象】（分块返回内容），而非一次性完整响应
# 5. 初始化full_ai_reply：流式返回的是文字碎片，必须拼接成完整AI回复，才能正确存入上下文
# 6. 打印提示前缀：用户体验优化，避免混淆AI回复和用户输入
# 7. 遍历chunk并处理：
#    - 遍历chunk：生成器是可迭代对象，每个chunk是AI刚生成的1-5个文字（或符号）
#    - 处理None：API的chunk里只有delta.content是文字，其他元数据（如finish_reason）的content是None，跳过避免报错
#    - end=""：让每个chunk的文字直接接在后面，不会每字占一行
#    - flush=True：强制Python立即把内容输出到终端（而非等缓冲区满），是实现【逐字蹦出来】的关键
# 8. 完整AI回复追加到messages：保证多轮对话上下文连贯——下一轮AI能看到自己之前的回复
# 9. 打印换行：UI优化，给下一轮对话留出清晰的分隔，提升可读性
