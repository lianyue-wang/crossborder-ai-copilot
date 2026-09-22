# ============================================
# 装饰器从零讲透
# 核心：装饰器本质就是"把原函数包一层，不改原函数代码，加新功能"
# ============================================

# ========== 第一步：函数就是变量 ==========
# 在 Python 里，函数和数字、字符串一样，可以赋值给变量

def say_hello():
    return "你好"

# 把函数赋值给另一个变量（注意不要加括号，加括号就执行了）
greet = say_hello

print(greet())      # 你好  —— greet 现在就是 say_hello

# 你之前学的 map(lambda x: x*2, nums)，就是把函数当参数传


# ========== 第二步：函数可以当参数 ==========
# 你已经学过 call_func 了

def add_one(x):
    return x + 1

def run_twice(func, n):
    """接收一个函数，调用它两次"""
    result1 = func(n)       # 第一次调用
    result2 = func(result1) # 第二次调用
    return result2

print(run_twice(add_one, 5))   # 7（5→6→7）


# ========== 第三步：函数里面可以定义函数 ==========

def outer():
    print("我是外层函数")

    def inner():            # 函数里面再定义一个函数
        print("我是内层函数")

    inner()                 # 在外层调用内层

outer()
# 输出：我是外层函数 / 我是内层函数


# ========== 第四步：函数可以返回函数 ==========
# 这是装饰器的关键！

def make_greeter():
    def greet():
        print("你好！")
    return greet            # 把函数本身返回（不加括号）

g = make_greeter()          # g 拿到了 greet 函数
g()                         # 你好！


# ========== 第五步：装饰器的本质（手动版，没有@） ==========
# 需求：想在每个函数执行前后打印日志，但不改原函数代码

def my_decorator(func):
    """接收一个函数，返回一个新函数"""

    def wrapper():
        print("--- 函数开始执行了 ---")
        func()              # 调用原来的函数
        print("--- 函数执行结束了 ---")

    return wrapper          # 返回包装后的新函数


def say_bye():
    print("再见！")

# 手动装饰：把原函数传给装饰器，拿到新函数
say_bye = my_decorator(say_bye)

say_bye()
# 输出：
# --- 函数开始执行了 ---
# 再见！
# --- 函数执行结束了 ---

# 原函数代码一行没改，但功能变了！这就是装饰器。


# ========== 第六步：@ 语法糖 ==========
# 上面手动写的  say_bye = my_decorator(say_bye)
# 可以简写为在函数上面加一行  @my_decorator

@my_decorator
def say_thanks():
    print("谢谢！")

say_thanks()
# 输出：
# --- 函数开始执行了 ---
# 谢谢！
# --- 函数执行结束了 ---

# @my_decorator 完全等价于 say_thanks = my_decorator(say_thanks)


# ========== 第七步：带参数的函数怎么装饰 ==========
# wrapper 要接收参数，传给原函数

def log_decorator(func):
    def wrapper(a, b):          # 接收和原函数一样的参数
        print(f"调用 {func.__name__}，参数是 {a}, {b}")
        result = func(a, b)     # 把参数传给原函数
        print(f"结果是 {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

add(3, 5)
# 输出：
# 调用 add，参数是 3, 5
# 结果是 8


# ========== 第八步：你项目里会遇到的 ==========
# LangChain 的 @tool 就是个装饰器！
# 它接收你的普通函数，把它"包装"成 LLM 能调用的工具

def my_tool(func):
    """假装这是LangChain的@tool"""
    func.is_tool = True         # 给函数加个标记
    return func

@my_tool
def calculate_profit(price, cost):
    """计算利润"""
    return price - cost

print(calculate_profit.is_tool)     # True（被装饰器标记成工具了）
print(calculate_profit(99, 30))      # 69（函数本身还能用）


# ========== 总结：装饰器干了什么 ==========
# 1. 接收一个函数
# 2. 定义一个 wrapper 函数，在里面"包"原函数
# 3. 返回 wrapper
# 4. @decorator 语法糖帮你自动完成  func = decorator(func)
#
# 一句话：装饰器 = 在不改原函数代码的前提下，给它加新功能（日志/计时/权限检查等）
