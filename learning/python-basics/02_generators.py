"""
Python 生成器学习脚本
=====================
目标：能看懂 yield，能自己写生成器，理解惰性求值

运行方式：
  .\\venv\\Scripts\\python.exe learning\\python-basics\\02_generators.py

为什么要学生成器：
- 你项目里处理大量商品数据/评论时，用生成器省内存
- LangChain 里的 LLM 流式输出本质就是生成器（astream()）
- 很多 Python 高级特性（async、上下文管理器）都基于生成器
"""

# ============================================================
# 一、什么是生成器？和普通函数的区别
# ============================================================
# 普通函数：return 返回结果，函数结束，局部变量销毁
# 生成器：yield 返回结果，函数暂停，下次调用从暂停处继续

def count_up_to(n):
    """普通函数：一次性生成所有数字，返回列表"""
    result = []
    for i in range(1, n + 1):
        result.append(i)
    return result

def count_up_to_gen(n):
    """生成器：每次 yield 一个，不占内存"""
    for i in range(1, n + 1):
        yield i  # 关键：yield 不是 return

# 对比
nums_list = count_up_to(5)       # 返回 [1,2,3,4,5]，占内存
nums_gen = count_up_to_gen(5)    # 返回生成器对象，几乎不占内存

print(type(nums_gen))  # <class 'generator'>

# 生成器是可迭代对象，可以用 for 遍历
for num in nums_gen:
    print(num, end=" ")  # 1 2 3 4 5
print()

# 也可以用 next() 逐个取
nums_gen2 = count_up_to_gen(3)
print(next(nums_gen2))  # 1
print(next(nums_gen2))  # 2
print(next(nums_gen2))  # 3
# print(next(nums_gen2))  # 再取会抛 StopIteration


# ============================================================
# 二、生成器的核心优势：惰性求值 + 省内存
# ============================================================
# 场景：读取一个10GB的日志文件，找包含"ERROR"的行

def read_errors_normal(filepath):
    """普通写法：一次性读所有行到列表，内存爆炸"""
    errors = []
    with open(filepath) as f:
        for line in f:
            if "ERROR" in line:
                errors.append(line)
    return errors  # 可能有几百万行，全在内存里

def read_errors_gen(filepath):
    """生成器写法：每次只 yield 一行，内存占用恒定"""
    with open(filepath) as f:
        for line in f:
            if "ERROR" in line:
                yield line  # 读完这行就暂停，下次再读下一行

# 你项目里的应用场景：
# - 遍历10万条评论做情感分析，用生成器逐条处理
# - 爬虫分页获取数据，用生成器 yield 每一页
# - LLM 流式输出，astream() 就是生成器，逐字 yield


# ============================================================
# 三、生成器表达式（一行写完）
# ============================================================
# 列表推导式用 []，生成器表达式用 ()

# 列表推导式：一次性生成所有平方数，占内存
squares_list = [x**2 for x in range(1000000)]
print(f"列表占用: {squares_list.__sizeof__()} 字节")  # 很大

# 生成器表达式：惰性求值，几乎不占内存
squares_gen = (x**2 for x in range(1000000))
print(f"生成器占用: {squares_gen.__sizeof__()} 字节")  # 很小

# 用法一样
for sq in squares_gen:
    if sq > 100:
        break
    print(sq, end=" ")
print()

# 常用场景：sum/max/min 可以直接吃生成器
total = sum(x**2 for x in range(1000))  # 不需要先建列表
print(f"平方和: {total}")


# ============================================================
# 四、yield from：委托给子生成器
# ============================================================
# 场景：生成器A里要遍历生成器B的所有元素

def flatten(nested):
    """普通写法：嵌套循环 yield"""
    for sublist in nested:
        for item in sublist:
            yield item

def flatten_v2(nested):
    """用 yield from：等价于上面的嵌套循环"""
    for sublist in nested:
        yield from sublist  # 委托给 sublist 这个可迭代对象

data = [[1, 2], [3, 4], [5]]
print(list(flatten(data)))    # [1, 2, 3, 4, 5]
print(list(flatten_v2(data))) # [1, 2, 3, 4, 5]


# ============================================================
# 五、生成器的高级方法：send / throw / close
# ============================================================
# 生成器不只能"产出"数据，还能"接收"数据（双向通信）

def echo_generator():
    """接收外部发送的值，加倍后返回"""
    while True:
        received = yield  # 暂停，等待外部 send 数据
        if received is None:
            break
        yield received * 2

gen = echo_generator()
next(gen)           # 必须先 next 启动，执行到第一个 yield 暂停
print(gen.send(10)) # 发送 10，生成器收到后加倍返回 20
next(gen)           # 继续到下一个 yield
print(gen.send(5))  # 发送 5，返回 10
gen.close()         # 关闭生成器

# 你项目里的应用：
# LangChain 的 Agent 工具调用循环，本质就是 send 工具结果给 LLM 继续推理


# ============================================================
# 六、itertools 标准库（生成器工具箱，必须认识）
# ============================================================
import itertools

# count：无限计数
# for i in itertools.count(1, 2):  # 1, 3, 5, 7, ...
#     print(i)

# cycle：无限循环
# for item in itertools.cycle(["A", "B"]):  # A, B, A, B, ...

# islice：切片生成器（生成器本身不能用 [1:3] 切片）
gen = (x for x in range(10))
first_3 = itertools.islice(gen, 3)  # 取前3个
print(list(first_3))  # [0, 1, 2]

# chain：拼接多个可迭代对象
chained = itertools.chain([1, 2], "abc", (3, 4))
print(list(chained))  # [1, 2, 'a', 'b', 'c', 3, 4]

# groupby：分组（需要先排序）
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]


# ============================================================
# 七、实战：用生成器处理你项目里的场景
# ============================================================

# 场景1：批量处理评论，逐条做情感分析，不占内存
def process_reviews(reviews):
    """逐条处理评论，yield 分析结果"""
    for review in reviews:
        # 模拟调用 LLM 分析
        sentiment = "positive" if "good" in review.lower() else "negative"
        yield {"review": review, "sentiment": sentiment}

reviews = ["Good product", "Bad quality", "Very good", "Terrible"]
for result in process_reviews(reviews):
    print(result)

# 场景2：分页爬取数据，用生成器 yield 每一页
def paginate(url, page_size=20):
    page = 1
    while True:
        # data = requests.get(f"{url}?page={page}&size={page_size}").json()
        data = [f"item_{page}_{i}" for i in range(page_size)]  # 模拟
        if not data:
            break
        yield data  # yield 这一页的数据
        page += 1
        if page > 3:  # 模拟只有3页
            break

for page_data in paginate("http://api.example.com/items"):
    print(f"获取到 {len(page_data)} 条数据")


# ============================================================
# 八、常见坑
# ============================================================
# 1. 生成器只能遍历一次 → 遍历完就空了，需要重新创建
#    gen = (x for x in range(3))
#    list(gen)  # [0,1,2]
#    list(gen)  # [] 空了！

# 2. 生成器没有 len() → 要用 sum(1 for _ in gen) 或先转 list

# 3. 生成器表达式作为函数参数时，括号可以省略
#    sum(x**2 for x in range(10))  # 正确
#    sum((x**2 for x in range(10)))  # 也对，但多了括号

# 4. yield 在 try/finally 里要小心 → close() 会触发 GeneratorExit

# 5. 不要在生成器里 return 值 → return 会结束生成器，值要通过 yield 返回


# ============================================================
# 九、练习题
# ============================================================

# 练习1：写一个生成器 fibonacci()，无限产出斐波那契数列
# 提示：a, b = b, a + b
"""
for n in fibonacci():
    if n > 100:
        break
    print(n)
# 期望: 1 1 2 3 5 8 13 21 34 55 89
"""

# 练习2：写一个生成器 chunked(iterable, size)，把可迭代对象按 size 分组
# 提示：用 itertools.islice
"""
list(chunked([1,2,3,4,5,6,7], 3))
# 期望: [[1,2,3], [4,5,6], [7]]
"""

# 练习3：写一个生成器 read_lines(filepath)，逐行读取文件，跳过空行和注释行(#开头)
# 提示：if line.strip() and not line.startswith("#"): yield line

# 练习4：看懂下面代码，说出输出（不要运行，先猜）
"""
def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print(next(g))
print(list(g))
print(list(g))
# 你的答案：?
"""

print("\n=== 生成器学习完成 ===")
print("下一步：做练习题，然后运行 03_async.py")
