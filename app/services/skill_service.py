from __future__ import annotations

import re


SKILL_PATTERNS = {
    "Python": [
        "python",
        "python 3",
    ],
    "Java": [
        "java",
    ],
    "C++": [
        "c++",
    ],
    "C#": [
        "c#",
    ],
    "JavaScript": [
        "javascript",
        "js",
    ],
    "TypeScript": [
        "typescript",
    ],
    "HTML": [
        "html",
        "html5",
    ],
    "CSS": [
        "css",
    ],
    "React": [
        "react",
        "react.js",
        "reactjs",
    ],
    "Node.js": [
        "node.js",
        "nodejs",
    ],
    "Flask": [
        "flask",
    ],
    "Django": [
        "django",
    ],
    "FastAPI": [
        "fastapi",
        "fast api",
    ],
    "REST API": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
    ],
    "SQL": [
        "sql",
    ],
    "MySQL": [
        "mysql",
    ],
    "PostgreSQL": [
        "postgresql",
        "postgres",
    ],
    "SQLite": [
        "sqlite",
    ],
    "SQLAlchemy": [
        "sqlalchemy",
    ],
    "MongoDB": [
        "mongodb",
        "mongo db",
    ],
    "Git": [
        "git",
        "github",
    ],
    "Docker": [
        "docker",
    ],
    "AWS": [
        "aws",
        "amazon web services",
    ],
    "Azure": [
        "azure",
    ],
    "Pandas": [
        "pandas",
    ],
    "NumPy": [
        "numpy",
    ],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn",
    ],
    "TensorFlow": [
        "tensorflow",
    ],
    "Machine Learning": [
        "machine learning",
        "ml",
    ],
    "NLP": [
        "nlp",
        "natural language processing",
    ],
    "Data Analysis": [
        "data analysis",
        "data analytics",
    ],
    "Analytics": [
        "analytics",
    ],
    "Power BI": [
        "power bi",
    ],
    "Tableau": [
        "tableau",
    ],
    "Excel": [
        "excel",
    ],
}


def _normalize_keyword(keyword: str) -> str:
    """Normalize a skill keyword before building a regex pattern."""
    return keyword.lower().strip()


def extract_skills(text: str) -> list[str]:
    """
    Extract known skills from text using dictionary-based matching.

    Returns a sorted list of canonical skill names.
    """
    if not text:
        return []

    normalized_text = re.sub(r"\s+", " ", text.lower()).strip()
    detected_skills = set()

    for skill_name, keywords in SKILL_PATTERNS.items():
        for keyword in keywords:
            normalized_keyword = _normalize_keyword(keyword)

            if not normalized_keyword:
                continue

            pattern = rf"(?<![a-z]){re.escape(normalized_keyword)}(?![a-z])"

            if re.search(pattern, normalized_text):
                detected_skills.add(skill_name)
                break

    return sorted(detected_skills)