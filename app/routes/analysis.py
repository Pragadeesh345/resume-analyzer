from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pypdf.errors import PdfReadError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import AnalysisResult, ResumeRecord
from app.schemas import AnalysisResponse, ResumeUploadResponse
from app.services.analysis_service import build_resume_analysis
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter()
settings = get_settings()
BASE_DIR = Path(__file__).resolve().parents[2]
MAX_JOB_DESCRIPTION_LENGTH = 50_000


def _remove_uploaded_file(file_path: Path) -> None:
    try:
        file_path.unlink(missing_ok=True)
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to clean up the uploaded file.",
        ) from exc


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": settings.APP_NAME}


@router.post("/resumes/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)) -> ResumeUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="A PDF file is required.")

    suffix = Path(file.filename).suffix.lower()
    if suffix != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_bytes = await file.read(settings.MAX_UPLOAD_SIZE_BYTES + 1)
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Resume file must be smaller than {settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB.",
        )
    if not file_bytes.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")

    upload_dir = Path(settings.UPLOAD_DIR)
    if not upload_dir.is_absolute():
        upload_dir = BASE_DIR / upload_dir
    try:
        upload_dir.mkdir(exist_ok=True)
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to prepare resume storage.",
        ) from exc

    stored_name = f"{uuid4().hex}.pdf"
    file_path = upload_dir / stored_name

    try:
        file_path.write_bytes(file_bytes)
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to store the uploaded resume.",
        ) from exc

    try:
        extracted_text = extract_text_from_pdf(file_path)
    except (PdfReadError, ValueError, OSError) as exc:
        _remove_uploaded_file(file_path)
        raise HTTPException(
            status_code=400,
            detail="Unable to extract readable text from the uploaded PDF.",
        ) from exc

    resume_record = ResumeRecord(
        filename=file.filename,
        stored_name=stored_name,
        file_size=len(file_bytes),
        extracted_text=extracted_text,
    )
    try:
        db.add(resume_record)
        db.commit()
        db.refresh(resume_record)
    except SQLAlchemyError as exc:
        db.rollback()
        _remove_uploaded_file(file_path)
        raise HTTPException(
            status_code=500,
            detail="Unable to save the uploaded resume.",
        ) from exc

    return ResumeUploadResponse(
        id=resume_record.id,
        filename=resume_record.filename,
        file_size=resume_record.file_size,
        extracted_text_preview=extracted_text[:500],
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume_id: int = Form(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    if (
        not job_description
        or len(job_description.strip()) < 10
        or len(job_description) > MAX_JOB_DESCRIPTION_LENGTH
    ):
        raise HTTPException(status_code=400, detail="Please provide a valid job description.")

    resume_record = db.get(ResumeRecord, resume_id)
    if not resume_record:
        raise HTTPException(status_code=404, detail="Resume not found.")

    resume_text = resume_record.extracted_text
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="The uploaded resume does not contain readable text.")

    try:
        analysis = build_resume_analysis(resume_text, job_description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = AnalysisResult(
        resume_id=resume_record.id,
        job_description=job_description,
        matched_skills=",".join(analysis["matched_skills"]),
        missing_skills=",".join(analysis["missing_skills"]),
        resume_only_skills=",".join(analysis["resume_only_skills"]),
        strengths="|".join(analysis["strengths"]),
        improvement_areas="|".join(analysis["improvement_areas"]),
        suggestions="|".join(analysis["suggestions"]),
        match_score=analysis["match_score"],
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return AnalysisResponse(
        id=result.id,
        resume_id=result.resume_id,
        match_score=result.match_score,
        matched_skills=[item for item in analysis["matched_skills"] if item],
        missing_skills=[item for item in analysis["missing_skills"] if item],
        resume_only_skills=[item for item in analysis["resume_only_skills"] if item],
        strengths=analysis["strengths"],
        improvement_areas=analysis["improvement_areas"],
        suggestions=analysis["suggestions"],
        job_description=job_description,
    )


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)) -> AnalysisResponse:
    result = db.get(AnalysisResult, analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found.")

    return AnalysisResponse(
        id=result.id,
        resume_id=result.resume_id,
        match_score=result.match_score,
        matched_skills=[s for s in result.matched_skills.split(",") if s],
        missing_skills=[s for s in result.missing_skills.split(",") if s],
        resume_only_skills=[s for s in result.resume_only_skills.split(",") if s],
        strengths=[s for s in result.strengths.split("|") if s],
        improvement_areas=[s for s in result.improvement_areas.split("|") if s],
        suggestions=[s for s in result.suggestions.split("|") if s],
        job_description=result.job_description,
    )
