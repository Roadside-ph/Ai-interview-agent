import asyncio
import time 

async def task(name:str, seconds:int) -> str:
    """模拟一个耗时任务"""
    print(f"任务{name}开始，需要{seconds}秒")
    await asyncio.sleep(seconds)
    print(f"任务{name}完成")
    return f"{name}的结果"

async def main():
    print(f"并发任务")
    start = time.time()

    results = await asyncio.gather(
        task("A",2),
         task("B",3),
          task("C",1),
    )
    
    end = time.time()
    print(f"任务完成，耗时{end - start:.2f}")

asyncio.run(main())