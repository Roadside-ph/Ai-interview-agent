# Prompt 模板管理
# 把所有 Prompt 集中管理，方便修改和复用

# 简历解析 Prompt
RESUME_PARSE_PROMPT = """你是一个专业的简历解析助手。
请解析以下简历内容，提取关键信息。

要求：
1. 严格按照 JSON 格式输出
2. 不要输出任何额外文字，只输出 JSON
3. 如果某个字段简历中没有提到，填 null

输出格式：
{{
  "name": "姓名",
  "education": ["学历+学校+专业"],
  "skills": ["技能1", "技能2"],
  "experience_years": 工作年限整数,
  "project_summary": ["项目经历简述1", "项目经历简述2"]
}}

简历内容：
{resume_text}"""

# JD（岗位描述）解析 Prompt
JD_PARSE_PROMPT = """你是一个专业的岗位分析助手。
请解析以下岗位描述（JD），提取关键要求。

要求：
1. 严格按照 JSON 格式输出
2. 不要输出任何额外文字，只输出 JSON

输出格式：
{{
  "job_title": "岗位名称",
  "required_skills": ["必备技能1", "必备技能2"],
  "preferred_skills": ["加分技能1", "加分技能2"],
  "experience_years": 要求年限整数,
  "education_requirement": "学历要求"
}}

岗位描述：
{jd_text}"""

# 岗位匹配 Prompt
MATCHING_PROMPT = """你是一个专业的岗位匹配分析师。
请根据候选人的简历信息和岗位要求，分析匹配度。

要求：
1. 严格按照 JSON 格式输出
2. 不要输出任何额外文字，只输出 JSON

输出格式：
{{
  "match_score": 匹配度百分比整数,
  "strengths": ["优势1", "优势2"],
  "weaknesses": ["短板1", "短板2"],
  "interview_topics": ["建议面试方向1", "建议面试方向2"]
}}

候选人信息：
{resume_info}

岗位要求：
{jd_info}"""
