"""测试 @timer 装饰器"""

import asyncio                    # 异步编程模块
from app.timer import timer       # 从 timer.py 导入我们写的装饰器


@timer                            # 语法糖，等价于 slow_task = timer(slow_task)
async def slow_task():
    """一个模拟的慢任务"""
    print("开始执行...")
    await asyncio.sleep(2)        # 异步等待 2 秒（模拟耗时操作）
    print("执行完成")
    return "done"                 # 返回结果


async def main():
    """主函数：调用被装饰的函数"""
    print("=== 测试 @timer 装饰器 ===")
    result = await slow_task()    # 调用时，timer 会自动记录耗时
    print(f"返回值: {result}")     # 打印 slow_task 的返回值


# 启动异步程序
asyncio.run(main())
