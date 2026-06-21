class AppError(Exception):
    pass

class APIError(AppError):
    pass

class APITimeoutError(APIError):
    pass

class HttpError(APIError):
    def __init__(self, message:str, status_code:int, response_text: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

class NetworkError(APIError): 
    pass

class ConfigError(AppError):
    pass