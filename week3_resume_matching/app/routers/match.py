from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.resume import JobInfo, MatchResult
from app.schemas.response import ApiResponse
from app.prompts import JD_PARSE_PROMPT, MATCHING_PROMPT
from app.llm_client import DeepSeekClient
from app.config import load_config

router = APIRouter(prefix="/matching", tags=["岗位匹配"])

class JDRequest(BaseModel):
    jd_text:str
    
@router.post("/parse-jd", response_model=ApiResponse)
async def parse_jd(req:JDRequest):

    config = load_config()
    client = DeepSeekClient(config)

    prompt = JD_PARSE_PROMPT.format(jd_text=req.jd_text)

    messages = [{"role":"user", "content":prompt}]
    result = await client.chat_with_schema(messages, JobInfo)
    
    await client.aclose()
    return ApiResponse(
        code=200,
        message="JD解析成功",
        data = result
    )

class MatchRequest(BaseModel):
    resume_info:str
    jd_info:str    

@router.post("/match", response_model=ApiResponse)
async def match_resume_jd(req:MatchRequest):

    config = load_config()
    client = DeepSeekClient(config)

    prompt = MATCHING_PROMPT.format(
        resume_info = req.resume_info,
        jd_info=req.jd_info
        )

    messages = [{"role":"user", "content":prompt}]
    result = await client.chat_with_schema(messages, MatchResult)
    
    await client.aclose()
    return ApiResponse(
        code=200,
        message="岗位匹配分析成功",
        data = result
    )