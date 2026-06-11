"""耗时统计装饰器"""

import time          # 时间模块，用来获取当前时间戳
import functools     # 工具模块，用来保留原函数信息


def timer(func):
    """装饰器工厂：接收一个函数，返回一个新函数（带有计时功能）"""
    
    @functools.wraps(func)  # 保留原函数的 __name__（名字）和 __doc__（文档字符串）
    async def wrapper(*args, **kwargs):
        # wrapper 是"包装函数"，会替换掉原函数
        
        start = time.time()                   # 记录函数执行前的时间（秒，浮点数）
        result = await func(*args, **kwargs)  # 执行原函数，*args 解包位置参数，**kwargs 解包关键字参数
        end = time.time()                     # 记录函数执行后的时间
        
        # 计算耗时并打印，func.__name__ 是原函数的名字
        print(f"{func.__name__} 耗时: {end - start:.2f} 秒")
        
        return result  # 把原函数的返回值传出去
    
    return wrapper  # 返回包装后的函数，而不是原函数
