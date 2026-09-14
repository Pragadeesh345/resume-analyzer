# Resume Analyzer

Resume Analyzer is a lightweight FastAPI application that helps a user compare a resume against a job description using transparent skill matching and an explainable match score.

## Problem Statement

Job applicants often need a quick and understandable way to check whether their resume aligns with a target role. Many existing tools are either too complex, too opaque, or require a cloud-based AI service. This project keeps the workflow local and understandable while still showing a practical resume-to-job comparison pipeline.

## Features

- Upload a resume in PDF format
- Extract text from the uploaded PDF
- Normalize and process the extracted text
- Parse a target job description
- Detect relevant skills from both resume and job description
- Compute a transparent Resume-JD Match Score
- List matched and missing skills
- Highlight strengths and improvement areas
- Generate practical suggestions for resume improvement
- Expose a simple REST API and a basic frontend
- Store resume metadata and analysis results in a local database

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- pypdf
- SQLite (local default, easy to run with no extra setup)
- HTML, CSS, JavaScript
- Pytest

## Architecture

The project follows a small backend structure:

- Frontend: browser-based form that uploads resume and job description
- API layer: FastAPI routes for upload and analysis
- Services layer: PDF extraction, text normalization, skill detection, and score generation
- Data layer: SQLAlchemy models and local SQLite database

## Workflow

1. User uploads a PDF resume.
2. The backend validates the file and extracts text.
3. The extracted text is normalized for readability.
4. User enters or pastes a job description.
5. The system identifies relevant technical skills from both sources.
6. Resume skills are compared against job skills.
7. A transparent match score is computed.
8. The API returns matched skills, missing skills, strengths, improvement areas, and suggestions.
9. The results are displayed in the browser.

## Folder Structure

```text
resume-analyzer/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── analysis.py
│   └── services/
│       ├── analysis_service.py
│       ├── pdf_service.py
│       ├── skill_service.py
│       └── text_service.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── tests/
│   ├── test_analysis_service.py
│   └── test_api.py
├── uploads/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

## Installation

1. Clone or open the project folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment.

On Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a local environment file:

```bash
copy .env.example .env
```

6. Start the app:

```bash
uvicorn app.main:app --reload
```

7. Open the frontend at:

```text
http://127.0.0.1:8000/
```

## Environment Setup

The default configuration uses SQLite for easy local development:

```env
APP_NAME=Resume Analyzer
DATABASE_URL=sqlite:///./resume_analyzer.db
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_BYTES=10485760
```

If a MySQL setup is needed later, the application can be adjusted with a different SQLAlchemy connection string.

## API Endpoints

### GET /health
Returns the app status.

### POST /resumes/upload
Uploads a PDF resume and stores the file with metadata.

### POST /analyze
Accepts a resume ID and a job description, then returns a structured analysis result.

### GET /analysis/{analysis_id}
Fetches a saved analysis record.

## Match Score Formula

The score is intentionally simple and transparent:

```text
Match Score = (Matched relevant skills / Required JD skills) x 100
```

This makes the result explainable and easy to discuss in interviews.

## Example Usage

1. Open the app in the browser.
2. Upload a resume PDF.
3. Paste a job description.
4. Click Analyze Resume.
5. Review the matched skills, missing skills, strengths, and suggestions.

## Limitations

- The skill detection is rule-based and dictionary-driven rather than fully semantic.
- PDF text extraction depends on the quality of the source document.
- The system does not claim to be a full ATS engine or a production-grade recruiter platform.
- LLM-based suggestions are intentionally planned as an optional future extension, not a hard dependency.

## Future Improvements

- Add a richer skill dictionary for more industries
- Support more document types beyond PDF
- Add better resume section extraction (projects, experience, education)
- Add optional LLM-powered suggestions with strict validation
- Support MySQL in production deployment
- Add user authentication and saved analysis history

## Testing

Run the automated tests with:

```bash
pytest -q
```

## Git Commit Suggestion

A meaningful milestone commit would be:

```bash
git add .
git commit -m "Initial Resume Analyzer setup with upload and skill matching"
```

## Security Note

This project keeps data local for development and avoids hardcoded secrets. It does not expose sensitive internal details and validates input before processing.

Uploaded resumes are limited to 10 MB by default, checked for a PDF signature, and stored using generated filenames rather than the original filename.
