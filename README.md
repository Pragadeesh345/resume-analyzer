# Resume Analyzer

A lightweight, API-driven application that analyzes a resume against a target job description using **rule-based skill extraction, transparent match scoring, and actionable improvement suggestions**.

Resume Analyzer helps job seekers identify relevant skills, recognize gaps, and better understand how their resume aligns with a specific role.

## 📌 Overview

Applying for jobs often means tailoring a resume to different job descriptions. Resume Analyzer simplifies this process by extracting text from a PDF resume, identifying relevant skills, and comparing them with the requirements of a target role.

The application combines a FastAPI backend, document-processing services, a skill-matching pipeline, and a browser-based interface to provide an explainable resume-to-job comparison workflow.

## ✨ Key Features

* **PDF Resume Processing** — Upload a resume and extract its text.
* **Text Preprocessing** — Normalize extracted text before analysis.
* **Job Description Analysis** — Process job descriptions to identify relevant skills.
* **Skill Extraction** — Detect skills using a predefined, rule-based skill dictionary.
* **Resume–Job Match Score** — Calculate a transparent score based on matched skills.
* **Skill Gap Analysis** — Identify matching and missing skills.
* **Improvement Suggestions** — Highlight strengths and potential areas for improvement.
* **REST API** — Expose resume upload and analysis functionality through FastAPI endpoints.
* **Persistent Storage** — Store resume metadata and analysis results using SQLAlchemy and SQLite.
* **Automated Testing** — Use Pytest to test application services and API behavior.

## 🏗️ Architecture

The application follows a modular, service-oriented structure that separates request handling, business logic, document processing, and data persistence.

```text
                    ┌────────────────────────┐
                    │   Browser Interface    │
                    │     HTML / CSS / JS    │
                    └───────────┬────────────┘
                                │ HTTP Requests
                                ▼
                    ┌────────────────────────┐
                    │     FastAPI Backend    │
                    │   Routes & Validation  │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │    Analysis Services   │
                    │                        │
                    │  • PDF Text Extraction │
                    │  • Text Preprocessing  │
                    │  • Skill Identification│
                    │  • Match Score         │
                    │  • Suggestions         │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │   Data Access Layer    │
                    │ SQLAlchemy + SQLite    │
                    └────────────────────────┘
```

### Architecture Components

| Component        | Responsibility                                                            |
| ---------------- | ------------------------------------------------------------------------- |
| Frontend         | Collect resume and job description inputs and display analysis results.   |
| API Layer        | Handle HTTP requests, validate inputs, and return structured responses.   |
| PDF Service      | Extract text from uploaded PDF resumes.                                   |
| Text Service     | Normalize extracted text for subsequent processing.                       |
| Skill Service    | Identify relevant skills using predefined matching rules.                 |
| Analysis Service | Compare resume and job-description skills and generate analysis results.  |
| Data Layer       | Persist resume metadata and analysis records using SQLAlchemy and SQLite. |

## 🔄 Analysis Workflow

1. **Resume Upload:** The user uploads a PDF resume through the application.
2. **File Validation:** The backend validates the uploaded file before processing.
3. **Text Extraction:** The PDF service extracts readable text from the document.
4. **Text Preprocessing:** The extracted content is normalized for analysis.
5. **Job Description Input:** The user provides the target job description.
6. **Skill Identification:** The system identifies relevant skills in both texts using a predefined dictionary.
7. **Skill Comparison:** The extracted resume skills are compared with the job requirements.
8. **Score Calculation:** The system calculates a match score based on the identified skills.
9. **Result Generation:** The application returns matched skills, missing skills, strengths, and improvement suggestions.
10. **Result Display:** The frontend presents the analysis to the user.

## 🛠️ Technology Stack

| Technology            | Purpose                                    |
| --------------------- | ------------------------------------------ |
| Python                | Core application logic and text processing |
| FastAPI               | REST API development                       |
| SQLAlchemy            | Database interaction and ORM               |
| Pydantic              | Data validation and structured schemas     |
| pypdf                 | PDF text extraction                        |
| SQLite                | Local data persistence                     |
| HTML, CSS, JavaScript | Browser-based frontend                     |
| Pytest                | Automated testing                          |

## 📁 Project Structure

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
├── pytest.ini
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

* Python 3.10 or a compatible version supported by the project's dependencies
* Git
* A web browser

### 1. Clone the Repository

```bash
git clone https://github.com/Pragadeesh345/resume-analyzer.git
cd resume-analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

**Windows — Command Prompt:**

```cmd
.venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a local `.env` file from the example:

```cmd
copy .env.example .env
```

The default development configuration uses SQLite. Check `.env.example` and `app/config.py` for the variables the application actually reads.

### 6. Start the Application

```bash
uvicorn app.main:app --reload
```

### 7. Open the Application

Visit the local application in your browser:

**http://127.0.0.1:8000/**

## 🔌 API Endpoints

| Method | Endpoint                  | Purpose                                              |
| ------ | ------------------------- | ---------------------------------------------------- |
| `GET`  | `/health`                 | Check application health.                            |
| `POST` | `/resumes/upload`         | Upload a PDF resume and store its metadata.          |
| `POST` | `/analyze`                | Analyze a resume against a supplied job description. |
| `GET`  | `/analysis/{analysis_id}` | Retrieve a saved analysis record.                    |

The API is designed to provide structured responses for the frontend and other potential clients.

For interactive API documentation, open **http://127.0.0.1:8000/docs** after starting the application, if the documentation endpoint is enabled.

## 📊 Match Score Calculation

The application uses a rule-based scoring approach:

```text
Match Score (%) =
(Number of Matched Relevant Skills / Number of Required Job Skills) × 100
```

For example, if a job description contains 10 identified required skills and the resume matches 6 of them:

```text
Match Score = (6 / 10) × 100 = 60%
```

The score provides a simple, interpretable indication of skill overlap. It is **not a prediction of hiring success or a measure of overall candidate suitability**.

## 🧪 Testing

Run the automated test suite from the project root:

```bash
pytest -q
```

The repository includes tests for analysis logic and API behavior. Run the tests locally to verify the current implementation.

## 🔐 Security and File Handling

* Environment-specific configuration can be maintained in a local `.env` file.
* The `.env` file and virtual environment should remain excluded from version control.
* Uploaded PDF files are subject to the application's file validation and size limits.
* Generated filenames help avoid relying on the original uploaded filename for storage.
* Resume content may contain personal information; use test documents when demonstrating the project publicly.

The default maximum upload size is **10 MB**, according to the application's documented configuration. Verify the current implementation before changing this limit.

## ⚠️ Current Limitations

* Skill identification relies on predefined dictionaries and matching rules rather than deep semantic understanding.
* PDF extraction quality depends on the document's structure and readability.
* The match score measures identified skill overlap, not the full context of a candidate's qualifications.
* The application is a resume-analysis prototype, not a complete Applicant Tracking System (ATS).
* LLM-powered analysis is a potential future enhancement, not a required part of the current workflow.

## 🚀 Future Enhancements

* Expand the skill dictionary to cover additional technical and non-technical roles.
* Improve extraction of resume sections such as education, experience, and projects.
* Support additional document formats.
* Explore semantic skill matching to recognize related skills and alternative terminology.
* Add optional LLM-assisted suggestions with appropriate validation.
* Add authentication and more advanced analysis-history management.
* Evaluate deployment and production database options.