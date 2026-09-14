from app.services.analysis_service import build_resume_analysis
from app.services.skill_service import extract_skills


def test_skill_extraction_and_match_score():
    resume = """
    Python developer with SQL, MySQL, REST APIs, Git, HTML, CSS and JavaScript experience.
    """

    jd = """
    Looking for a developer with Python, SQL, MySQL, REST API, Git,
    HTML, CSS and JavaScript skills.
    """

    result = build_resume_analysis(resume, jd)

    assert result["match_score"] == 100.0
    assert set(result["matched_skills"]) == {
        "Python",
        "SQL",
        "MySQL",
        "REST API",
        "Git",
        "HTML",
        "CSS",
        "JavaScript",
    }
    assert result["missing_skills"] == []


def test_missing_skills_are_reported():
    resume = """
    Python developer with SQL and MySQL experience.
    """

    jd = """
    Looking for a developer with Python, SQL, MySQL, FastAPI and Docker.
    """

    result = build_resume_analysis(resume, jd)

    assert set(result["matched_skills"]) == {
        "Python",
        "SQL",
        "MySQL",
    }

    assert set(result["missing_skills"]) == {
        "FastAPI",
        "Docker",
    }


def test_rest_api_variations_are_detected_as_same_skill():
    text = """
    Experience with REST API, REST APIs, RESTful API and RESTful APIs.
    """

    skills = extract_skills(text)

    assert skills.count("REST API") == 1
    assert "REST API" in skills


def test_fastapi_variations_are_detected():
    text = """
    Experience with FastAPI and Fast API development.
    """

    skills = extract_skills(text)

    assert skills.count("FastAPI") == 1
    assert "FastAPI" in skills


def test_skill_matching_normalizes_repeated_spaces_and_line_breaks():
    text = """
    Experience with Fast
    API, REST    API, and Machine
    Learning.
    """

    skills = extract_skills(text)

    assert "FastAPI" in skills
    assert "REST API" in skills
    assert "Machine Learning" in skills


def test_postgresql_variations_are_detected_as_same_skill():
    text = """
    Experience with PostgreSQL and Postgres databases.
    """

    skills = extract_skills(text)

    assert skills.count("PostgreSQL") == 1
    assert "PostgreSQL" in skills


def test_github_is_detected_as_git():
    text = """
    The project source code is maintained on GitHub.
    """

    skills = extract_skills(text)

    assert "Git" in skills