from __future__ import annotations

from app.services.skill_service import extract_skills


def build_resume_analysis(resume_text: str, job_description: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    if not jd_skills:
        raise ValueError("No relevant skills could be detected in the job description.")

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)
    resume_only_skills = sorted(resume_skills - jd_skills)

    match_score = round((len(matched_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0.0

    strengths = []
    if matched_skills:
        strengths = [f"Strong alignment with {skill} requirements." for skill in matched_skills[:5]]
    else:
        strengths = ["The resume does not yet show clear overlap with the job requirements."]

    improvement_areas = [
        f"Consider adding evidence of experience with {skill} in your projects or experience section."
        for skill in missing_skills[:5]
    ] or ["Add more concrete examples of technical work to improve alignment with the target role."]

    suggestions = []
    for skill in missing_skills[:5]:
        suggestions.append(
            f"If you have relevant experience with {skill}, highlight it in your skills, projects, or work experience section."
        )
    if not suggestions:
        suggestions = ["Your resume already covers the main job requirements. Focus on improving clarity and measurable project impact."]

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_only_skills": resume_only_skills,
        "strengths": strengths,
        "improvement_areas": improvement_areas,
        "suggestions": suggestions,
        "match_score": match_score,
    }
