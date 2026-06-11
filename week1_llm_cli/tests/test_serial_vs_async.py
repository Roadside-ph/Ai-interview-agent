"""对比串行和并发的速度差异"""

import asyncio
from app.timer import timer       # 导入我们写的计时装饰器


async def slow_task(name: str, seconds: int):
    """模拟耗时任务
    
    Args:
        name: 任务名称（A、B、C）
        seconds: 模拟耗时秒数
    """
    print(f"任务 {name} 开始，需要 {seconds} 秒")
    await asyncio.sleep(seconds)   # 异步等待，模拟耗时操作
    print(f"任务 {name} 完成")
    return f"{name} 结果"


@timer                             # 用 @timer 装饰，自动统计整个函数耗时
async def serial_demo():
    """串行执行：一个一个来，必须等前一个完成才执行下一个"""
    print("=== 串行执行 ===")
    
    # await 是"等完成"的意思
    # 先等 A 完成（2秒），再等 B 完成（3秒），最后等 C 完成（1秒）
    await slow_task("A", 2)   # 等 2 秒
    await slow_task("B", 3)   # 再等 3 秒
    await slow_task("C", 1)   # 再等 1 秒
    # 总时间 = 2 + 3 + 1 = 6 秒


@timer                             # 用 @timer 装饰，自动统计整个函数耗时
async def concurrent_demo():
    """并发执行：同时进行，不用一个一个等"""
    print("=== 并发执行 ===")
    
    # asyncio.gather() 同时启动多个任务
    # 三个任务同时开始，谁先完成谁先返回
    await asyncio.gather(
        slow_task("A", 2),   # 任务 A：2 秒
        slow_task("B", 3),   # 任务 B：3 秒
        slow_task("C", 1),   # 任务 C：1 秒
    )
    # 总时间 ≈ max(2, 3, 1) = 3 秒（只等最慢的那个）


async def main():
    """主函数：先串行演示，再并发演示"""
    
    # 先跑串行版本
    await serial_demo()
    
    print("\n" + "=" * 30 + "\n")   # 分隔线
    
    # 再跑并发版本
    await concurrent_demo()


# 启动异步程序
asyncio.run(main())
