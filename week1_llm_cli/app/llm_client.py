"""llm客户端封装:封装Deepseek API调用"""
from app.api_client import APIClient
from app.config import AppConfig
from app.logger import setup_logger

logger = setup_logger("llm_cli.llm")

class LLMClient:
    def __init__(self,config:AppConfig) -> None:
        self.client = APIClient(config.base_url,timeout=60.0)
        self.model = config.model_name
        self.api_key = config.api_key
        logger.info(f"LLMClient初始化完成，模型：{config.model_name}")

    def chat(self,messages:list[dict[str,str]]) -> str:
        logger.info(f"调用LLM,消息数：{len(messages)}")
        result = self.client.post("/chat/completions",json_data={"model":self.model,"messages":messages},headers={"Authorization":f"Bearer {self.api_key}"})
        logger.info(f"LLM调用成功，回复长度{len(result)}字符")
        return result["choices"][0]["message"]["content"]
         