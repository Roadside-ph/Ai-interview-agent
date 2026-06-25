from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.llm_client import DeepSeekClient
from app.config import load_config

router = APIRouter(prefix="/chat", tags=["聊天"])

class ChatRequest(BaseModel):
    message: str

async def event_generator(message: str):
    config = load_config()
    client = DeepSeekClient(config)

    messages = [{"role": "user", "content": message}]

    try:
        async for chunk in client.chat_stream(messages):
            yield f"data: {chunk}\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n" 
    finally:
        await client.aclose()
        yield "data: [DONE]\n\n"

@router.post("/stream")
async def chat_stream(req:ChatRequest):
    return StreamingResponse(
        event_generator(req.message),
        media_type="text/event-stream"
    )