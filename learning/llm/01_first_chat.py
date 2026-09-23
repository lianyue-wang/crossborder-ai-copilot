# ============================================
# 第一个大模型调用：和 DeepSeek 聊天
# ============================================

# 第一步：读 API Key（从 .env 文件里读，不直接写在代码里）
from dotenv import load_dotenv
import os

load_dotenv()   # 读取项目根目录的 .env 文件

api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key: {api_key[:10]}...")   # 只打印前10位，不泄露完整key


# 第二步：创建客户端
# DeepSeek 兼容 OpenAI 的接口格式，所以直接用 OpenAI 的 SDK
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"   # DeepSeek 的地址
)


# 第三步：调用大模型
response = client.chat.completions.create(
    model="deepseek-chat",     # 模型名
    messages=[
        {"role": "user", "content": "我之前是一名2年工作经验的java程序员，但是技术比较菜只会crud，后面转行做了一年跨境电商产品开发，但是ai出来过后我手写了一个skill，ai智能体就能把我的工作做到百分之八十了我觉得肯定会被替代而且工资只有五千块，所以我现在在学python转行回去做ai应用开发，分析一下职业前景怎么样，"}
    ]
)

# 第四步：打印结果
print("\n=== 大模型回复 ===")
print(response.choices[0].message.content)

# 第五步：看 token 消耗（成本！）
print("\n=== Token 消耗 ===")
print(f"输入 token:  {response.usage.prompt_tokens}")
print(f"输出 token:  {response.usage.completion_tokens}")
print(f"总共 token: {response.usage.total_tokens}")
