from pydantic import BaseModel


class ResumeInfo(BaseModel):
    name: str | None = None
    education: list[str] | None = []
    skills: list[str] | None = []
    experience_years: int | None = None
    project_summary: list[str] | None = []


class JobInfo(BaseModel):
    job_title: str | None = None
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    experience_years: int | None = None
    education_requirement: str | None = None


class MatchResult(BaseModel):
    match_score: int = 0
    strengths: list[str] = []
    weaknesses: list[str] = []
    interview_topics: list[str] = []
