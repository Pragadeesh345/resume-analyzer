from __future__ import annotations
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.database import Base


class ResumeRecord(Base):
    __tablename__ = "resume_records"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    stored_name = Column(String(255), nullable=False, unique=True)
    file_size = Column(Integer, nullable=False)
    extracted_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resume_records.id"),
        index=True,
        nullable=False,
    )

    job_description = Column(Text, nullable=False)
    matched_skills = Column(Text, nullable=False)
    missing_skills = Column(Text, nullable=False)
    resume_only_skills = Column(Text, nullable=False)
    strengths = Column(Text, nullable=False)
    improvement_areas = Column(Text, nullable=False)
    suggestions = Column(Text, nullable=False)
    match_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)