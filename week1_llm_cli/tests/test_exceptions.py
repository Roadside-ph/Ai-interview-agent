"""测试自定义异常类的继承关系。"""

from app.exceptions import (
    AppError,
    APIError,
    APITimeoutError,
    HttpError,
    NetworkError,
    ConfigError,
)


def test_app_error_is_exception():
    """AppError 应该继承自 Exception"""
    assert issubclass(AppError, Exception)


def test_api_error_is_app_error():
    """APIError 应该继承自 AppError"""
    assert issubclass(APIError, AppError)


def test_timeout_error_is_api_error():
    """APITimeoutError 应该继承自 APIError"""
    assert issubclass(APITimeoutError, APIError)


def test_http_error_is_api_error():
    """HttpError 应该继承自 APIError"""
    assert issubclass(HttpError, APIError)


def test_network_error_is_api_error():
    """NetworkError 府该继承自 APIError"""
    assert issubclass(NetworkError, APIError)


def test_config_error_is_app_error():
    """ConfigError 应该继承自 AppError"""
    assert issubclass(ConfigError, AppError)


def test_http_error_has_attributes():
    """HttpError 应该能存储 status_code 和 response_text"""
    err = HttpError("测试错误", status_code=401, response_text="Unauthorized")
    assert err.status_code == 401
    assert err.response_text == "Unauthorized"
    assert str(err) == "测试错误"
