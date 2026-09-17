"""
Python async 异步编程学习脚本
=============================
目标：能看懂 async/await，能写异步函数，理解事件循环

运行方式：
  .\\venv\\Scripts\\python.exe learning\\python-basics\\03_async.py

为什么要学 async：
- FastAPI 路由默认推荐 async def
- LLM API 调用用 async 可以并发，速度快10倍
- LangChain 的 astream/ainvoke 都是异步方法
- 你项目里视频生成、批量选品都需要异步
"""

import asyncio
import time

# ============================================================
# 一、核心概念：同步 vs 异步
# ============================================================
# 同步：一件事做完再做下一件，等待时什么都不干
# 异步：等待时（比如等API响应）去做别的事，不浪费时间

def sync_task(name, seconds):
    """同步任务：sleep 时整个程序卡住"""
    print(f"{name} 开始，需要 {seconds} 秒")
    time.sleep(seconds)  # 同步等待，阻塞
    print(f"{name} 完成")
    return f"{name}结果"

async def async_task(name, seconds):
    """异步任务：sleep 时可以去做别的事"""
    print(f"{name} 开始，需要 {seconds} 秒")
    await asyncio.sleep(seconds)  # 异步等待，不阻塞
    print(f"{name} 完成")
    return f"{name}结果"

# 对比：3个任务各2秒
# 同步：2+2+2 = 6秒
# 异步：同时开始，最多2秒就全部完成


# ============================================================
# 二、async def 和 await（最基础的语法）
# ============================================================
# async def 定义协程函数，调用它返回协程对象，不会立即执行
# await 等待协程完成，获取返回值

async def simple_demo():
    print("开始")
    result = await async_task("任务A", 1)
    print(f"拿到结果: {result}")
    print("结束")

# 运行协程的入口：asyncio.run()
# asyncio.run(simple_demo())  # 取消注释运行


# ============================================================
# 三、并发执行：asyncio.gather（最常用）
# ============================================================
# 场景：同时调用3个LLM API，不用等一个完了再调下一个

async def concurrent_demo():
    start = time.time()

    # 方式1：顺序执行（慢，6秒）
    # await async_task("A", 2)
    # await async_task("B", 2)
    # await async_task("C", 2)

    # 方式2：并发执行（快，2秒）
    results = await asyncio.gather(
        async_task("A", 2),
        async_task("B", 2),
        async_task("C", 2),
    )
    print(f"所有结果: {results}")
    print(f"总耗时: {time.time() - start:.2f}秒")

# asyncio.run(concurrent_demo())
# 输出：
# A 开始，需要 2 秒
# B 开始，需要 2 秒
# C 开始，需要 2 秒
# A 完成
# B 完成
# C 完成
# 所有结果: ['A结果', 'B结果', 'C结果']
# 总耗时: 2.00秒


# ============================================================
# 四、asyncio.create_task：后台任务
# ============================================================
# 场景：启动一个后台任务（比如视频生成），不阻塞主流程

async def background_demo():
    # create_task 立即开始执行，不等待
    task = asyncio.create_task(async_task("后台视频生成", 3))

    # 主流程继续做别的事
    print("主流程：开始处理其他事情...")
    await asyncio.sleep(1)
    print("主流程：其他事情做完了")

    # 需要结果时再 await
    result = await task
    print(f"后台任务结果: {result}")

# asyncio.run(background_demo())


# ============================================================
# 五、实战：并发调用LLM API（你项目里的真实场景）
# ============================================================
# 场景：给10条评论做情感分析，逐条调用要10秒，并发只要1秒

async def analyze_review(review):
    """模拟调用LLM分析单条评论"""
    await asyncio.sleep(0.5)  # 模拟API耗时
    sentiment = "positive" if "good" in review.lower() else "negative"
    return {"review": review, "sentiment": sentiment}

async def analyze_reviews_batch(reviews):
    """并发分析所有评论"""
    start = time.time()
    tasks = [analyze_review(review) for review in reviews]
    results = await asyncio.gather(*tasks)
    print(f"分析 {len(reviews)} 条评论，耗时 {time.time() - start:.2f}秒")
    return results

# asyncio.run(analyze_reviews_batch(["good", "bad", "great", "terrible"]))
# 输出: 分析 4 条评论，耗时 0.50秒（不是2秒！）


# ============================================================
# 六、超时控制：asyncio.wait_for（API调用必备）
# ============================================================
# 场景：调用LLM API，超过5秒没响应就取消

async def api_call_with_timeout():
    try:
        result = await asyncio.wait_for(
            async_task("慢API", 10),  # 这个任务要10秒
            timeout=2                  # 但只等2秒
        )
    except asyncio.TimeoutError:
        print("API调用超时，已取消")
        # 这里可以做降级：切换备用模型或返回缓存

# asyncio.run(api_call_with_timeout())


# ============================================================
# 七、信号量：控制并发数（防API限流）
# ============================================================
# 场景：LLM API有QPS限制，不能同时发100个请求

async def analyze_with_semaphore(review, semaphore):
    async with semaphore:  # 最多同时5个
        return await analyze_review(review)

async def rate_limited_demo():
    semaphore = asyncio.Semaphore(5)  # 最多5个并发
    reviews = [f"review_{i}" for i in range(20)]
    tasks = [analyze_with_semaphore(r, semaphore) for r in reviews]
    results = await asyncio.gather(*tasks)
    print(f"完成 {len(results)} 条，每批最多5个并发")

# asyncio.run(rate_limited_demo())


# ============================================================
# 八、async for：异步迭代器（流式输出的底层）
# ============================================================
# LLM 的 astream() 就是异步生成器，用 async for 逐字接收

async def async_stream_generator():
    """模拟LLM流式输出，逐字返回"""
    for char in "Hello, AI!":
        await asyncio.sleep(0.1)  # 模拟每个字的生成间隔
        yield char

async def stream_demo():
    async for char in async_stream_generator():
        print(char, end="", flush=True)  # 逐字打印
    print()

# asyncio.run(stream_demo())
# 输出: H e l l o ,   A I ! （逐字出现）


# ============================================================
# 九、FastAPI 里的 async（你项目里的写法）
# ============================================================
# FastAPI 路由函数用 async def，框架自动管理事件循环
#
# from fastapi import FastAPI
# app = FastAPI()
#
# @app.post("/api/generate-listing")
# async def generate_listing(product: ProductInfo):
#     # 并发调用：标题生成 + 五点描述 + A+文案
#     title, bullets, a_plus = await asyncio.gather(
#         generate_title(product),
#         generate_bullets(product),
#         generate_a_plus(product),
#     )
#     return {"title": title, "bullets": bullets, "a_plus": a_plus}
#
# 关键点：
# - 路由函数用 async def
# - 调用 LLM 用 await llm.ainvoke(...)
# - 多个独立任务用 asyncio.gather 并发
# - 不要在 async 函数里用 time.sleep()，要用 await asyncio.sleep()
# - 不要在 async 函数里调用同步的阻塞IO（比如 requests.get），要用 aiohttp


# ============================================================
# 十、常见坑（90%的初学者会踩）
# ============================================================

# 坑1：调用 async 函数不加 await → 只创建协程对象，不执行
"""
async def foo():
    return 42

result = foo()  # ❌ result 是协程对象，不是42
print(result)   # <coroutine object foo at 0x...>

result = await foo()  # ✅ result 是42
"""

# 坑2：在 async 函数里用同步阻塞调用 → 整个事件循环卡住
"""
async def bad():
    time.sleep(2)       # ❌ 阻塞整个事件循环，其他任务都等
    requests.get(url)   # ❌ 同步HTTP请求，阻塞

async def good():
    await asyncio.sleep(2)  # ✅ 异步等待
    await aiohttp.get(url)  # ✅ 异步HTTP
"""

# 坑3：忘记 asyncio.run() → 协程不会执行
"""
async def main():
    print("hello")

main()  # ❌ 什么都不输出，只是创建了协程对象
asyncio.run(main())  # ✅ 输出 hello
"""

# 坑4：gather 里一个任务失败 → 全部取消
# 解决：加 return_exceptions=True
"""
results = await asyncio.gather(task1, task2, return_exceptions=True)
# 失败的任务返回 Exception 对象，不会影响其他任务
"""

# 坑5：CPU密集型任务用 async 没用 → async 只对IO密集型有效
# 计算密集型要用多进程（multiprocessing），不是 async


# ============================================================
# 十一、同步代码和异步代码混用
# ============================================================
# 场景：你有一个同步函数（比如用 requests 调API），想在 async 里用

def sync_api_call():
    """同步函数，阻塞"""
    time.sleep(1)
    return "同步结果"

async def mixed_demo():
    # 方式1：用 asyncio.to_thread 把同步函数放到线程池执行
    result = await asyncio.to_thread(sync_api_call)
    print(f"同步函数异步执行结果: {result}")

    # 方式2：如果是第三方库只提供同步接口，用 to_thread 包装
    # 不要直接调用，会阻塞事件循环

# asyncio.run(mixed_demo())


# ============================================================
# 十二、练习题
# ============================================================

# 练习1：写一个异步函数 fetch_all(urls)，并发请求所有URL，返回结果列表
# 提示：用 asyncio.gather，每个任务用 aiohttp 或模拟 asyncio.sleep
"""
async def fetch_all(urls):
    # 你的代码
    pass

results = asyncio.run(fetch_all(["url1", "url2", "url3"]))
"""

# 练习2：给练习1加超时控制，每个请求最多等3秒，超时返回"timeout"
# 提示：用 asyncio.wait_for + try/except

# 练习3：写一个异步生成器 stream_tokens(text)，每隔0.1秒 yield 一个字符
# 然后用 async for 逐字打印
"""
async def stream_tokens(text):
    # 你的代码
    pass

asyncio.run(stream_and_print("Hello World"))
"""

# 练习4：看懂下面代码，说出总耗时（不要运行，先猜）
"""
async def task():
    await asyncio.sleep(1)
    return "done"

async def main():
    start = time.time()
    t1 = asyncio.create_task(task())
    t2 = asyncio.create_task(task())
    await t1
    await t2
    print(f"耗时: {time.time() - start:.2f}秒")

asyncio.run(main())
# 你的答案：?秒
"""

# 练习5：把练习4改成顺序执行（不用 create_task），耗时是多少？
"""
async def main():
    start = time.time()
    await task()
    await task()
    print(f"耗时: {time.time() - start:.2f}秒")
# 你的答案：?秒
"""


# ============================================================
# 运行演示
# ============================================================
if __name__ == "__main__":
    print("=== 运行并发演示 ===")
    asyncio.run(concurrent_demo())

    print("\n=== 运行流式输出演示 ===")
    asyncio.run(stream_demo())

    print("\n=== async 学习完成 ===")
    print("关键点回顾：")
    print("1. async def 定义协程，await 等待结果")
    print("2. asyncio.gather 并发执行多个任务")
    print("3. create_task 启动后台任务")
    print("4. wait_for 超时控制，Semaphore 限流")
    print("5. async for 遍历异步生成器（LLM流式输出）")
    print("6. 不要在 async 里用同步阻塞调用（time.sleep/requests）")
