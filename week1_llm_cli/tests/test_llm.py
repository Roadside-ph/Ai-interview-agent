from app.config import load_config
from app.llm_client import LLMClient

config = load_config()
client = LLMClient(config)

messages = [{"role":"user","content":"你好，请用一句话介绍你自己"}]
reply = client.chat(messages)

print("AI回复：",reply)
