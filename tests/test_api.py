from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client(tmp_path) -> Generator[TestClient, None, None]:
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        test_engine.dispose()


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_rejects_non_pdf_files(client: TestClient) -> None:
    response = client.post(
        "/resumes/upload",
        files={"file": ("resume.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed."


def test_upload_rejects_fake_pdf_content(client: TestClient) -> None:
    response = client.post(
        "/resumes/upload",
        files={"file": ("resume.pdf", b"not a real pdf", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The uploaded file is not a valid PDF."


def test_analysis_requires_existing_resume(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        data={
            "resume_id": "999999",
            "job_description": "Python backend developer role",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found."


def test_upload_requires_file(client: TestClient) -> None:
    response = client.post("/resumes/upload")

    assert response.status_code == 422


def test_analysis_rejects_short_job_description(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        data={
            "resume_id": "999999",
            "job_description": "Python",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Please provide a valid job description."
    )


def test_analysis_rejects_non_numeric_resume_id(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        data={
            "resume_id": "abc",
            "job_description": "Python backend developer role",
        },
    )

    assert response.status_code == 422

def test_analysis_rejects_empty_job_description(client: TestClient) -> None:
    response = client.post(
        "/analyze",
        data={
            "resume_id": "999999",
            "job_description": "",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Please provide a valid job description."
    )


def test_analysis_rejects_job_description_over_50000_characters(
    client: TestClient,
) -> None:
    response = client.post(
        "/analyze",
        data={
            "resume_id": "999999",
            "job_description": "Python " + ("backend " * 6250),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Please provide a valid job description."
    )