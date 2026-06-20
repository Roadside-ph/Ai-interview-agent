"""日志配置模块：统一管理项目的日志输出。

使用方式：
    from app.logger import setup_logger
    logger = setup_logger()
    logger.info("程序启动")
    logger.error("出错了")

日志级别（从低到高，越低越详细）：
    DEBUG    - 调试信息，开发时用
    INFO     - 普通运行信息
    WARNING  - 警告，不影响运行但要注意
    ERROR    - 错误，某个操作失败
    CRITICAL - 严重错误，程序可能无法继续
"""

import logging


def setup_logger(name: str = "ai_interview") -> logging.Logger:
    """
    创建并配置一个 Logger 实例。

    Args:
        name: Logger 名称，一般用项目名来区分日志来源

    Returns:
        配置好的 Logger 对象
    """
    # 获取（或创建）一个名为 name 的 Logger
    # 同一个 name 多次调用会返回同一个对象，不会重复创建
    logger = logging.getLogger(name)

    # 防止重复添加 handler
    # 因为 getLogger 同名返回同一对象，不检查的话会叠加 handler，
    # 导致同一条日志输出多次
    if logger.handlers:
        return logger

    # 设置 Logger 的最低级别为 DEBUG（全部放行）
    # 具体哪些显示取决于下面 Handler 的级别
    logger.setLevel(logging.DEBUG)

    # ========== 控制台输出 ==========
    # StreamHandler = 输出到终端控制台
    console_handler = logging.StreamHandler()

    # 控制台级别设为 INFO（比 DEBUG 高）
    # 所以 DEBUG 级别的日志不会显示在控制台
    console_handler.setLevel(logging.INFO)

    # ========== 日志格式 ==========
    # 常用占位符：
    #   %(asctime)s   - 时间
    #   %(levelname)s - 级别名称（INFO/ERROR 等）
    #   -8s           - 左对齐，占 8 个字符宽度（让级别名对齐）
    #   %(name)s      - Logger 名称
    #   %(module)s    - 模块文件名（不含 .py）
    #   %(message)s   - 日志内容
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s.%(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 把格式绑定到控制台 Handler
    console_handler.setFormatter(formatter)

    # 把控制台 Handler 挂到 Logger 上
    logger.addHandler(console_handler)

    # ========== 文件输出 ==========
    # FileHandler = 把日志写入文件，方便事后排查
    # "app.log" 是文件名，会在运行目录下自动创建
    # encoding="utf-8" 防止中文乱码
    file_handler = logging.FileHandler("app.log", encoding="utf-8")

    # 文件级别设为 DEBUG（最低级别）
    # 这样控制台看不到的 DEBUG 信息，文件里也有记录
    file_handler.setLevel(logging.DEBUG)

    # 用同一个格式
    file_handler.setFormatter(formatter)

    # 把文件 Handler 也挂到 Logger 上
    logger.addHandler(file_handler)

    return logger
