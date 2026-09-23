# ============================================
# 04 Token与成本 —— 每次对话花了多少钱
# 学习日期：9.25 周五（3h）
# ============================================

# 【学习目标】
# 1. 理解什么是Token
# 2. 看懂 usage 里的三个数字
# 3. 写一个成本计算函数

# 【核心概念】
# Token = 大模型计费的最小单位，不是"字"也不是"词"
#   - 1个中文字 ≈ 1-2个token
#   - 1个英文单词 ≈ 1个token
#
# DeepSeek定价（2026年）：
#   输入（prompt）：¥1 / 百万token
#   输出（completion）：¥2 / 百万token

# ========== 初始化 ==========
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ========== 你的任务 ==========

# 任务1：写一个 calculate_cost(usage) 函数
#   输入：一个usage对象（从response.usage拿）
#   返回：本次调用花了多少钱（元）
#   公式：(输入token × 1 + 输出token × 2) / 1000000
#   usage里有什么：usage.prompt_tokens（输入）、usage.completion_tokens（输出）

# 任务2：调一次API，然后打印：
#   - AI回复内容
#   - 输入token数
#   - 输出token数
#   - 总token数
#   - 本次花了多少钱（用你刚写的函数）

# 任务3：思考这个问题（写在注释里）
#   如果每天100个用户，每人聊20轮，每轮平均输入500、输出200 token
#   一个月花多少钱？

# ============================================
# 【验收标准】
# ✅ 能说出token是什么
# ✅ 能说出输入和输出分别怎么计费
# ✅ calculate_cost函数能正确算出成本
# ✅ 跑完测试能看到具体的token数和金额
# ============================================
