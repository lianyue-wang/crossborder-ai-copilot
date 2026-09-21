"""
Python 装饰器学习脚本
=====================
目标：能看懂别人写的装饰器，能自己写简单装饰器

运行方式：在项目根目录执行
  .\\venv\\Scripts\\python.exe learning\\python-basics\\01_decorators.py

学习方法：
1. 先读注释理解概念
2. 取消注释每个示例的调用代码，运行看输出
3. 做末尾的练习题
"""

# ============================================================
# 一、核心概念：函数是"一等公民"
# ============================================================
# 在Python里，函数和变量一样，可以：
# - 赋值给变量
# - 作为参数传给另一个函数
# - 作为返回值从函数里返回
# - 定义在另一个函数内部（闭包）
#
# 装饰器本质：一个函数，接收另一个函数作为参数，返回一个新函数（通常是包装后的）

def greet(name):
    return f"Hello, {name}!"

# 函数可以赋值给变量
say_hello = greet
print(say_hello("Alice"))  # 输出: Hello, Alice!

# 函数可以作为参数传递
def call_func(func, arg):
    return func(arg)

print(call_func(greet, "Bob"))  # 输出: Hello, Bob!


# ============================================================
# 二、最简单的装饰器（手写版）
# ============================================================
# 需求：在不修改 greet 函数代码的前提下，给它加上"执行前打印日志"的功能

def my_decorator(func):
    """接收一个函数，返回一个包装后的新函数"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] 准备调用 {func.__name__}")
        result = func(*args, **kwargs)  # 调用原函数
        print(f"[LOG] {func.__name__} 调用完成，结果: {result}")
        return result
    return wrapper  # 返回包装函数（注意：不调用，只是返回）

# 用法1：手动包装（理解原理用）
greet_with_log = my_decorator(greet)
print(greet_with_log("Charlie"))
# 输出:
# [LOG] 准备调用 greet
# [LOG] greet 调用完成，结果: Hello, Charlie!
# Hello, Charlie!


# ============================================================
# 三、语法糖 @decorator（实际项目都这么写）
# ============================================================

@my_decorator  # 等价于 greet2 = my_decorator(greet2)
def greet2(name):
    return f"Hi, {name}!"

print(greet2("David"))
# 输出和上面一样，自动加了日志


# ============================================================
# 四、functools.wraps（必须加，否则有坑）
# ============================================================
# 问题：被装饰后的函数，__name__ 和 __doc__ 会变成 wrapper 的
# 解决：用 @functools.wraps(func) 保留原函数的元信息

import functools

def my_decorator_v2(func):
    @functools.wraps(func)  # 关键：保留原函数名和文档
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator_v2
def greet3(name):
    """这是一个打招呼函数"""
    return f"Hey, {name}!"

print(greet3.__name__)  # 输出: greet3（不加wraps会输出 wrapper）
print(greet3.__doc__)   # 输出: 这是一个打招呼函数


# ============================================================
# 五、带参数的装饰器
# ============================================================
# 需求：装饰器本身可以接收参数，比如指定日志级别

def log_with_level(level):
    """外层函数接收装饰器参数，返回真正的装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] 调用 {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_with_level("INFO")   # 先调用 log_with_level("INFO") 返回 decorator，再装饰
def func_a():
    return "A done"

@log_with_level("DEBUG")
def func_b():
    return "B done"

print(func_a())  # [INFO] 调用 func_a
print(func_b())  # [DEBUG] 调用 func_b


# ============================================================
# 六、实战常用装饰器（必须看懂）
# ============================================================

# 1. 计时装饰器
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} 耗时 {end - start:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "finished"

print(slow_function())  # 取消注释看效果


# 2. 重试装饰器（API调用必备，你项目里会用到）
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise  # 最后一次失败，抛出异常
                    print(f"[RETRY] 第{attempt}次失败: {e}，{delay}秒后重试")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def call_api():
    # 模拟前两次失败
    if not hasattr(call_api, "count"):
        call_api.count = 0
    call_api.count += 1
    if call_api.count < 3:
        raise ConnectionError("API超时")
    return "成功"

# print(call_api())  # 取消注释看重试效果


# 3. 缓存装饰器（标准库自带，比自己写好）
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# print(fibonacci(100))  # 不加缓存会算死，加了瞬间出结果


# ============================================================
# 七、类装饰器（了解，能看懂就行）
# ============================================================
# 用类实现装饰器，需要实现 __call__ 方法

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[COUNT] {self.func.__name__} 已调用 {self.count} 次")
        return self.func(*args, **kwargs)

@CountCalls
def say_hi():
    return "hi"

# say_hi()  # 第1次
# say_hi()  # 第2次
# print(say_hi.count)  # 2


# ============================================================
# 八、常见坑
# ============================================================
# 1. 忘记 @functools.wraps → 函数名变成 wrapper，调试困难
# 2. 装饰器返回值丢失 → wrapper 必须 return func(...) 的结果
# 3. 带参数装饰器少写一层 → 必须是三层嵌套（参数→装饰器→wrapper）
# 4. 装饰器在导入时就执行 → 装饰器内部逻辑不要写太重的东西
# 5. 多个装饰器顺序 → 从下往上执行（离函数最近的先执行）


# ============================================================
# 九、练习题（动手写，不要只看）
# ============================================================

# 练习1：写一个 @debug 装饰器，打印函数名、参数、返回值
# 提示：用 func.__name__, args, kwargs, result
"""
@debug
def add(a, b):
    return a + b
add(3, 5)
# 期望输出: [DEBUG] add(a=3, b=5) -> 8
"""

# 练习2：写一个 @slow_down(seconds) 装饰器，调用函数前等待指定秒数
# 提示：带参数装饰器，三层嵌套

# 练习3：写一个 @run_times(n) 装饰器，让被装饰函数执行n次，返回最后一次结果
# 提示：循环调用 func(*args, **kwargs)

# 练习4：看懂下面代码，说出输出顺序（不要运行，先猜）
"""
def deco1(func):
    def wrapper():
        print("deco1 before")
        func()
        print("deco1 after")
    return wrapper

def deco2(func):
    def wrapper():
        print("deco2 before")
        func()
        print("deco2 after")
    return wrapper

@deco1
@deco2
def target():
    print("target")

target()
# 你的答案：?
"""

print("\n=== 装饰器学习完成 ===")
print("下一步：做练习题，然后运行 02_generators.py")
