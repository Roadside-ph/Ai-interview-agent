"""测试日志配置模块。"""

from app.logger import setup_logger


def test_setup_logger_returns_logger():
    """setup_logger 应该返回一个 Logger 对象"""
    logger = setup_logger("test_logger")
    assert logger is not None
    assert logger.name == "test_logger"


def test_setup_logger_default_name():
    """不传参数时，默认名称应该是 llm_cli"""
    logger = setup_logger()
    assert logger.name == "llm_cli"


def test_setup_logger_no_duplicate_handlers():
    """多次调用 setup_logger 同一个 name，不应该重复添加 handler"""
    # 先清理已有 handler（避免其他测试的干扰）
    logger = setup_logger("test_no_dup")
    handler_count = len(logger.handlers)

    # 再调用一次
    logger2 = setup_logger("test_no_dup")

    # 应该是同一个对象，handler 数量不变
    assert logger is logger2
    assert len(logger2.handlers) == handler_count
