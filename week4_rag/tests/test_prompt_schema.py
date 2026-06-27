# 测试 Prompt 模板和 Pydantic 模型

from app.prompts import RESUME_PARSE_PROMPT, JD_PARSE_PROMPT, MATCHING_PROMPT
from app.schemas.resume import ResumeInfo, JobInfo, MatchResult


# 测试 1：Prompt 模板能填入变量
def test_prompt_template():
    # 把 {resume_text} 替换成真实内容
    prompt = RESUME_PARSE_PROMPT.format(resume_text="张三，清华大学本科，会 Python")
    assert "张三" in prompt
    assert "清华大学" in prompt
    print("✅ Prompt 模板变量替换正常")


# 测试 2：Pydantic 模型能校验正确数据
def test_resume_info_valid():
    data = {
        "name": "张三",
        "education": ["清华大学 本科"],
        "skills": ["Python", "Java"],
        "experience_years": 3,
        "project_summary": ["开发了 AI 面试系统"]
    }
    result = ResumeInfo(**data)
    assert result.name == "张三"
    assert len(result.skills) == 2
    print("✅ ResumeInfo 校验正确数据通过")


# 测试 3：Pydantic 模型能处理缺失字段
def test_resume_info_missing_fields():
    # 只传 name，其他字段用默认值
    data = {"name": "李四"}
    result = ResumeInfo(**data)
    assert result.name == "李四"
    assert result.skills == []
    assert result.experience_years is None
    print("✅ ResumeInfo 缺失字段用默认值填充")


# 测试 4：JobInfo 模型
def test_job_info():
    data = {
        "job_title": "AI Agent 开发工程师",
        "required_skills": ["Python", "LLM"],
        "preferred_skills": ["LangChain"],
        "experience_years": 1,
        "education_requirement": "本科及以上"
    }
    result = JobInfo(**data)
    assert result.job_title == "AI Agent 开发工程师"
    print("✅ JobInfo 校验通过")


# 测试 5：MatchResult 模型
def test_match_result():
    data = {
        "match_score": 85,
        "strengths": ["Python 基础扎实"],
        "weaknesses": ["缺少 LangChain 经验"],
        "interview_topics": ["异步编程", "FastAPI"]
    }
    result = MatchResult(**data)
    assert result.match_score == 85
    print("✅ MatchResult 校验通过")
