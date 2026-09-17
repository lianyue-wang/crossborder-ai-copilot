"""
Python 基础语法学习脚本（Java转Python专用）
==========================================
目标：从Java CRUD水平，快速掌握Python核心语法，能看懂能写

运行方式：
  .\\venv\\Scripts\\python.exe learning\\python-basics\\00_python_basics.py

学习方法：
1. 先读注释，对比Java的写法找差异
2. 取消注释每个示例，运行看输出
3. 做末尾练习题
4. 全部搞懂后再学 01_decorators.py
"""

# ============================================================
# 一、变量与数据类型
# ============================================================
# Python 不需要声明类型，直接赋值（动态类型）
# Java: int x = 10;  String name = "Alice";
# Python: x = 10    name = "Alice"

# 基本类型
age = 25                  # int 整数
price = 19.99             # float 浮点数
name = "Alice"            # str 字符串
is_active = True          # bool 布尔（首字母大写！Java是true）
nothing = None            # None 空值（Java的null）

print(type(age))          # <class 'int'>
print(type(price))        # <class 'float'>
print(type(name))         # <class 'str'>

# 类型转换
num_str = "123"
num_int = int(num_str)    # 字符串转整数
num_float = float(num_int) # 整数转浮点
back_to_str = str(num_int) # 数字转字符串

# f-string 格式化字符串（最常用，比Java的+拼接方便）
print(f"姓名: {name}, 年龄: {age}, 价格: {price:.2f}")
# 输出: 姓名: Alice, 年龄: 25, 价格: 19.99


# ============================================================
# 二、字符串操作
# ============================================================
s = "Hello, Python!"

print(len(s))              # 14 长度
print(s.upper())           # HELLO, PYTHON! 大写
print(s.lower())           # hello, python! 小写
print(s.replace("Python", "World"))  # Hello, World! 替换
print(s.split(","))        # ['Hello', ' Python!'] 分割
print(s.strip())           # 去首尾空格
print(s[0])                # H 索引（从0开始，和Java一样）
print(s[0:5])              # Hello 切片（左闭右开）
print(s[-1])               # ! 负数索引从末尾开始
print("Python" in s)       # True 包含判断

# 多行字符串
multi = """第一行
第二行
第三行"""
print(multi)


# ============================================================
# 三、列表 list（Java的ArrayList）
# ============================================================
fruits = ["apple", "banana", "cherry"]

print(fruits[0])           # apple 索引
print(fruits[-1])          # cherry 最后一个
print(fruits[0:2])         # ['apple', 'banana'] 切片
fruits.append("date")      # 末尾添加（Java的add）
fruits.insert(1, "blueberry")  # 指定位置插入
fruits.remove("banana")    # 删除指定元素
print(len(fruits))         # 长度
print("apple" in fruits)   # True 包含判断

# 遍历
for fruit in fruits:
    print(fruit)

# 带索引遍历（Java没有这个，很常用）
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# 排序
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                # 原地排序
print(sorted(nums))        # 返回新列表，不修改原列表
nums.reverse()             # 反转

# 列表推导式（Python特色，必须会）
# Java: List<Integer> squares = new ArrayList<>(); for(int x: nums) squares.add(x*x);
squares = [x**2 for x in range(10)]
print(squares)             # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件的推导式
evens = [x for x in range(10) if x % 2 == 0]
print(evens)               # [0, 2, 4, 6, 8]


# ============================================================
# 四、字典 dict（Java的HashMap）
# ============================================================
person = {
    "name": "Alice",
    "age": 25,
    "city": "成都"
}

print(person["name"])      # Alice 取值
person["email"] = "alice@example.com"  # 添加/修改
del person["age"]          # 删除
print(person.keys())       # dict_keys(['name', 'city', 'email'])
print(person.values())     # dict_values(['Alice', '成都', 'alice@example.com'])
print(person.items())      # 键值对

# 遍历
for key, value in person.items():
    print(f"{key}: {value}")

# 安全取值（key不存在不报错）
print(person.get("phone", "未知"))  # 未知（默认值）

# 字典推导式
square_dict = {x: x**2 for x in range(5)}
print(square_dict)         # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}


# ============================================================
# 五、元组 tuple 和 集合 set
# ============================================================
# 元组：不可变的列表（创建后不能修改）
point = (3, 4)
print(point[0])            # 3
x, y = point               # 解包（Java没有，很方便）
print(f"x={x}, y={y}")     # x=3, y=4

# 集合：无序不重复（Java的HashSet）
colors = {"red", "green", "blue", "red"}  # red重复会自动去重
print(colors)              # {'red', 'green', 'blue'}
colors.add("yellow")       # 添加
colors.remove("red")       # 删除


# ============================================================
# 六、条件与循环
# ============================================================
# if-elif-else（注意：用缩进代替Java的{}）
score = 85
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# for 循环（和Java的for-each一样，但没有for(int i=0;i<n;i++)写法）
for i in range(5):         # range(5) = 0,1,2,3,4
    print(i)

for i in range(1, 10, 2):  # 从1到9，步长2
    print(i)               # 1,3,5,7,9

# while 循环
count = 0
while count < 3:
    print(count)
    count += 1             # Python没有count++，要用count += 1

# break 和 continue（和Java一样）
for i in range(10):
    if i == 5:
        break              # 跳出循环
    if i % 2 == 0:
        continue           # 跳过本次
    print(i)               # 1,3


# ============================================================
# 七、函数
# ============================================================
# 基本函数
def greet(name):
    """函数文档字符串（Java的Javadoc）"""
    return f"Hello, {name}!"

print(greet("Bob"))

# 默认参数
def greet_with_default(name, greeting="Hello"):
    """带默认参数的打招呼函数。

    Args:
        name: 要打招呼的人名
        greeting: 问候语，默认为"Hello"

    Returns:
        拼接好的问候字符串
    """
    return f"{greeting}, {name}!"

print(greet_with_default("Alice"))           # Hello, Alice!
print(greet_with_default("Alice", "Hi"))     # Hi, Alice!
print("测试提交代码，苹果也太傻逼了")
# 关键字参数（调用时指定参数名，顺序可以乱）
def create_user(name, age, city="未知"):
    """创建用户信息字典。

    Args:
        name: 用户名
        age: 年龄
        city: 所在城市，默认为"未知"

    Returns:
        包含name/age/city的用户字典
    """
    return {"name": name, "age": age, "city": city}

print(create_user(age=25, name="Bob", city="成都"))  # 顺序可以乱

# *args：任意数量位置参数（Java的可变参数 String... args）
def sum_all(*args):
    """计算任意数量数字的总和。

    Args:
        *args: 任意数量的数字参数

    Returns:
        所有数字的和
    """
    return sum(args)

print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs：任意数量关键字参数
def print_info(**kwargs):
    """打印任意数量的关键字参数（键值对）。

    Args:
        **kwargs: 任意数量的关键字参数，如 name="Alice", age=25
    """
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="成都")

# lambda 匿名函数（Java的 -> 箭头函数）
square = lambda x: x**2
print(square(5))             # 25

# 常用高阶函数
nums = [1, 2, 3, 4, 5]
print(list(map(lambda x: x*2, nums)))     # [2,4,6,8,10] 映射
print(list(filter(lambda x: x > 3, nums))) # [4,5] 过滤


# ============================================================
# 八、类与对象
# ============================================================
class Person:
    # 类变量（所有实例共享，Java的static变量）
    species = "Human"

    def __init__(self, name, age):
        """构造方法（Java的构造函数），self相当于Java的this"""
        self.name = name       # 实例变量
        self.age = age

    def say_hello(self):
        """实例方法，第一个参数必须是self"""
        return f"我是{self.name}，今年{self.age}岁"

    # 静态方法（Java的static方法，不需要self）
    @staticmethod
    def is_adult(age):
        """判断是否成年（静态方法，不需要创建实例就能调用）。

        Args:
            age: 年龄

        Returns:
            成年返回True，否则False
        """
        return age >= 18

# 继承
class Student(Person):
    def __init__(self, name, age, school):
        """学生类构造方法，继承自Person。

        Args:
            name: 姓名
            age: 年龄
            school: 学校名称
        """
        super().__init__(name, age)  # 调用父类构造
        self.school = school

    def say_hello(self):
        """学生自我介绍（重写父类方法）。

        Returns:
            包含姓名和学校的自我介绍字符串
        """
        return f"我是{self.name}，在{self.school}上学"

# 使用
p = Person("Alice", 25)
print(p.say_hello())        # 我是Alice，今年25岁
print(Person.is_adult(25))  # True

s = Student("Bob", 20, "四川大学")
print(s.say_hello())        # 我是Bob，在四川大学上学
print(isinstance(s, Person))  # True（Student是Person的子类）


# ============================================================
# 九、异常处理
# ============================================================
# Java: try { ... } catch (Exception e) { ... } finally { ... }
# Python: try: ... except Exception as e: ... finally: ...

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"除零错误: {e}")
except (TypeError, ValueError) as e:
    print(f"类型或值错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
else:
    print("没有异常时执行")  # else是可选的，没有异常才执行
finally:
    print("无论如何都执行")  # 清理资源用

# 主动抛出异常（Java的throw）
def validate_age(age):
    """验证年龄是否合法，不合法则抛出异常。

    Args:
        age: 年龄

    Returns:
        合法的年龄

    Raises:
        ValueError: 年龄为负数时抛出
    """
    if age < 0:
        raise ValueError("年龄不能为负数")
    return age

# 自定义异常
class BusinessError(Exception):
    pass


# ============================================================
# 十、文件操作
# ============================================================
# 写入文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 读取文件（with自动关闭文件，Java的try-with-resources）
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()       # 读取全部
    print(content)

# 逐行读取（大文件用这个，省内存）
with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip()去掉换行符

# 清理测试文件
import os
os.remove("test.txt")


# ============================================================
# 十一、模块导入
# ============================================================
# import 模块名
import math
print(math.sqrt(16))        # 4.0

# from 模块 import 函数/类
from math import pi, sin
print(pi)                   # 3.141592653589793
print(sin(pi/2))            # 1.0

# 起别名
import numpy as np          # 常用别名，比如 pandas as pd, numpy as np

# 你项目里常用的导入
# from fastapi import FastAPI
# from langchain_openai import ChatOpenAI
# from pydantic import BaseModel
# import asyncio


# ============================================================
# 十二、常用内置函数（必须记住）
# ============================================================
print(len("hello"))         # 5 长度
print(range(5))             # range(0,5) 范围
print(enumerate(["a","b"])) # 带索引
print(zip([1,2], ["a","b"])) # 打包 [(1,'a'),(2,'b')]
print(max([3,1,4]))         # 4 最大值
print(min([3,1,4]))         # 1 最小值
print(sum([1,2,3]))         # 6 求和
print(abs(-5))              # 5 绝对值
print(round(3.14159, 2))    # 3.14 四舍五入
print(sorted([3,1,2]))      # [1,2,3] 排序
print(isinstance(5, int))   # True 类型判断
print(any([False, True]))   # True 任一为真
print(all([True, True]))    # True 全部为真


# ============================================================
# 十三、Python和Java的关键差异（容易踩坑）
# ============================================================
"""
差异点            Java                    Python
--------------    --------------------    --------------------
代码块            用 {} 大括号             用缩进（4个空格）
语句结束            分号 ;                  换行（不需要分号）
变量声明            int x = 10;            x = 10（自动推断）
布尔值              true / false            True / False（首字母大写）
空值                null                    None
自增                i++                     i += 1（没有++）
for循环             for(int i=0;i<n;i++)   for i in range(n):
字符串拼接          "a" + "b"              "a" + "b" 或 f"a{b}"
方法参数            按值传递               按对象引用传递
数组/列表           int[] arr = new int[]  arr = [1,2,3]（自动扩容）
字典/Map            HashMap<String,Integer> d = {"a": 1}
异常                try-catch-finally      try-except-finally
导入                import com.xxx.Class   from module import Class
"""


# ============================================================
# 十四、练习题（必须动手写）
# ============================================================

# 练习1：写一个函数，接收一个列表，返回其中所有偶数的平方和
# 提示：列表推导式 + sum()
"""
def sum_of_even_squares(nums):
    \"\"\"计算列表中所有偶数的平方和。

    Args:
        nums: 数字列表，如 [1,2,3,4,5,6]

    Returns:
        所有偶数的平方和，如 2²+4²+6² = 56
    \"\"\"
    # 你的代码
    pass

print(sum_of_even_squares([1,2,3,4,5,6]))  # 期望: 56 (4+16+36)
"""

# 练习2：写一个函数，接收一个字符串，返回每个单词出现次数的字典
# 提示：用 dict.get(word, 0) + 1
"""
def word_count(text):
    \"\"\"统计字符串中每个单词出现的次数。

    Args:
        text: 输入字符串，单词用空格分隔

    Returns:
        字典，key是单词，value是出现次数，如 {'hello': 2, 'world': 1}
    \"\"\"
    # 你的代码
    pass

print(word_count("hello world hello python"))
# 期望: {'hello': 2, 'world': 1, 'python': 1}
"""

# 练习3：写一个类 Calculator，有 add/subtract/multiply/divide 四个方法
# divide 要处理除零异常，返回 None 并打印错误
"""
class Calculator:
    # 你的代码
    pass

calc = Calculator()
print(calc.add(3, 5))       # 8
print(calc.divide(10, 0))   # 打印错误，返回 None
"""

# 练习4：用列表推导式，从下面列表中找出所有长度大于3的单词，转大写
"""
words = ["cat", "elephant", "dog", "tiger", "bird"]
# 你的代码，结果应该是 ['ELEPHANT', 'TIGER', 'BIRD']
"""

# 练习5：写一个函数，读取一个文件，统计行数（空行不算）
# 提示：with open + for line in f + if line.strip()
"""
def count_non_empty_lines(filepath):
    # 你的代码
    pass
"""


print("\n=== Python基础语法学习完成 ===")
print("下一步：做练习题，然后运行 01_decorators.py 学装饰器")
