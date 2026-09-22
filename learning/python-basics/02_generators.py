# ============================================
# 生成器（Generator）从零讲透
# 核心：生成器是"算一个给一个"的函数，不一次性算完存起来
# ============================================

# ========== 第一步：先看普通函数的问题 ==========

def make_list(n):
    """普通函数：一次性算出所有结果，存在列表里"""
    result = []
    for i in range(n):
        result.append(i * i)   # 全部算好存起来
    return result

# 一调用就把 1000000 个数全部算好，占一大块内存
nums = make_list(1000000)
print("普通函数前3个：", nums[:3])
# 问题：如果只要前3个，你白算了999997个


# ========== 第二步：生成器函数用 yield ==========

def make_generator(n):
    """生成器函数：每遇到 yield 就暂停，返回一个值"""
    for i in range(n):
        yield i * i            # 暂停在这，把 i*i 交出去
        # 下次再来时，从这里继续

# 调用生成器函数，不会立即执行，而是返回一个生成器对象
gen = make_generator(1000000)
print("生成器对象：", gen)

# 用 next() 取下一个值——每次只算一个！
print("第1个：", next(gen))    # 0
print("第2个：", next(gen))    # 1
print("第3个：", next(gen))    # 4


# ========== 第三步：yield 和 return 的区别 ==========

def normal_func():
    """普通函数：return 一次性返回，函数结束"""
    return 1
    return 2              # 永远不会执行，函数已经结束了

def gen_func():
    """生成器函数：yield 暂停，下次从暂停处继续"""
    yield 1               # 暂停，交出1
    yield 2               # 下次继续执行到这，交出2
    yield 3               # 再下次继续

g = gen_func()
print(next(g))    # 1
print(next(g))    # 2
print(next(g))    # 3
# 再 next(g) 就会报 StopIteration（没东西了）


# ========== 第四步：用 for 循环遍历生成器 ==========

# for 循环会自动不断调用 next()，直到生成器结束
for num in make_generator(5):
    print(num, end=" ")
# 输出：0 1 4 9 16
print()

# ========== 第五步：生成器表达式（你已经见过了） ==========

# 列表推导式 [ ]：一次性存所有结果
list_version = [x**2 for x in range(5)]
print("列表推导式：", list_version)     # [0, 1, 4, 9, 16]
print("类型：", type(list_version))      # <class 'list'>

# 生成器表达式 ( )：算一个给一个，不存
gen_version = (x**2 for x in range(5))
print("生成器表达式：", gen_version)     # <generator object ...>
print("类型：", type(gen_version))      # <class 'generator'>

# 在 sum() 里括号可以省略
total = sum(x**2 for x in range(1000))
print("平方和：", total)


# ========== 第六步：为什么要用生成器？省内存 ==========

import sys

# 存 100000 个数的列表
big_list = [x**2 for x in range(100000)]
print("列表占内存：", sys.getsizeof(big_list), "字节")

# 同样的数据，用生成器
big_gen = (x**2 for x in range(100000))
print("生成器占内存：", sys.getsizeof(big_gen), "字节")

# 列表占了 80 万字节，生成器只占 200 字节！
# 因为生成器不存数据，只记住"算到哪了"


# ========== 第七步：你项目里会用到的 ==========

# 大模型流式输出 astream() 就是生成器！
# LLM 不是一次性返回整段文章，而是一个字一个字往外蹦

def fake_llm_stream(prompt):
    """模拟大模型逐字输出"""
    words = ["你", "好", "，", "我", "是", "AI", "助", "手"]
    for word in words:
        yield word           # 吐一个字就暂停

# 就像 LLM.astream() 一样
for chunk in fake_llm_stream("你是谁"):
    print(chunk, end="", flush=True)   # 逐字打印
print()

# 对比：
# 普通调用：等10秒，一次性出完整文章
# 流式调用：第1秒出"你"，第2秒出"好"，用户不用干等


# ========== 总结 ==========
# 1. yield 代替 return：遇到 yield 暂停，下次继续
# 2. 生成器不一次性算完，算一个给一个
# 3. 省内存：100万个数也不占空间
# 4. 流式输出（astream）底层就是生成器
# 5. 生成器表达式：(x for x in ...) 没方括号
