# ============================================
# 05 CLI聊天机器人 v1.0 —— 整合前面所有知识
# 学习日期：9.26 周六（8h）
# ============================================

# 【学习目标】
# 把前三天的东西整合成一个完整的CLI聊天机器人
# 功能：多轮对话 + 流式输出 + Token统计 + 成本计算

# 【你需要整合的三个能力】
# 1. 多轮对话（来自02）：messages数组存历史
# 2. 流式输出（来自03）：stream=True逐字打印
# 3. Token成本（来自04）：每轮显示花了多少钱

# ========== 初始化（我只给你imports）==========
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ========== 你的任务 ==========

# 这个文件全部由你自己写。你需要实现：
#
# 1. 顶部打印欢迎信息
# 2. 维护 messages 列表（system角色：跨境电商选品顾问）
# 3. while循环：
#    - input获取用户输入
#    - "退出"：打印累计统计（总token、总成本），break
#    - "清空"：重置messages，continue
#    - 普通输入：
#      a. 用户消息append到messages
#      b. 用 stream=True 调API
#      c. 逐字打印AI回复，同时收集完整回复
#      d. 用 stream_options={"include_usage": True} 拿token数
#      e. AI回复append到messages
#      f. 打印本轮消耗（输入X + 输出Y token, ¥Z）
# 4. 维护累计统计：total_input_tokens, total_output_tokens, total_cost
#    定价：输入¥1/百万token，输出¥2/百万token

# 提示：
#   - 你已经在02写过多轮对话，在03写过流式，在04写过成本
#   - 这个文件就是把这三个拼在一起
#   - 流式模式下拿usage的方法：create时加 stream_options={"include_usage": True}
#     然后 for chunk in stream 时，最后一个 chunk 会有 .usage 属性

# ============================================
# 【验收标准】
# ✅ 多轮对话：连续聊10轮不丢上下文
# ✅ 流式输出：逐字蹦出来
# ✅ 每轮结束显示：本轮token数和花费
# ✅ 输入"清空"能重置对话
# ✅ 输入"退出"显示累计统计
# ✅ system角色生效：AI回答像选品顾问
# ============================================
