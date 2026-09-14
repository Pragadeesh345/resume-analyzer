import re


def normalize_text(text: str) -> str:
    if not text:
        return ""

    cleaned = text.replace("\r", "\n")
    cleaned = re.sub(r"\n+", "\n", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()