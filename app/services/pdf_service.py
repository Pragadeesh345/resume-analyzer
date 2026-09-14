from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from app.services.text_service import normalize_text


def extract_text_from_pdf(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    try:
        reader = PdfReader(str(file_path))
    except Exception as exc:  # pragma: no cover - defensive branch
        raise ValueError("Unable to read the uploaded PDF file.") from exc

    pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages.append(page_text)

    if not pages:
        raise ValueError("The PDF does not contain readable text.")

    combined_text = "\n".join(pages)
    return normalize_text(combined_text)
