from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
    file_size: int
    extracted_text_preview: str


class AnalysisRequest(BaseModel):
    resume_id: int = Field(..., gt=0)
    job_description: str = Field(..., min_length=10)


class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    resume_only_skills: list[str]
    strengths: list[str]
    improvement_areas: list[str]
    suggestions: list[str]
    job_description: str
