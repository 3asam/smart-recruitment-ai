import re
import pdfplumber
from typing import Dict, List, Optional


SKILLS_LIST = [
    "python", "java", "c++", "sql", "javascript",
    "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "react", "next.js", "node.js",
    "c#", "mongodb", "tailwind", "html", "css",
    "git", "rest apis", "jwt"
]


def extract_cv_data(file_path: str) -> Dict:
    """
    Main CV parsing function (ONLY entry point)
    """

    text = _extract_text_from_pdf(file_path)
    cleaned_text = _clean_text(text)

    return {
        "name": _extract_name(cleaned_text),
        "email": _extract_email(cleaned_text),
        "phone": _extract_phone(cleaned_text),
        "skills": _extract_skills(cleaned_text),
        "experience": _extract_experience(cleaned_text),
        "education": _extract_education(cleaned_text),
    }


# -------------------------
# Helpers (Internal)
# -------------------------

def _extract_text_from_pdf(file_path: str) -> str:
    content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                content += page_text + "\n"
    return content


def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_email(text: str) -> Optional[str]:
    match = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text)
    return match.group(0) if match else None


def _extract_phone(text: str) -> Optional[str]:
    match = re.search(r"(\+?\d{1,3})?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}", text)
    return match.group(0) if match else None


def _extract_name(text: str) -> Optional[str]:
    lines = text.split("\n")
    if lines:
        candidate = lines[0].strip()
        if len(candidate.split()) <= 4:
            return candidate.title()
    return None


def _extract_skills(text: str) -> List[str]:
    found = []
    for skill in SKILLS_LIST:
        if skill in text:
            found.append(skill)
    return found


def _extract_experience(text: str) -> List[str]:
    experiences = []
    patterns = [
        r"\b\d+\s+years?\b",
        r"\bexperience\b.*?\."
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        experiences.extend(matches)
    return list(set(experiences))


def _extract_education(text: str) -> List[str]:
    education_keywords = [
        "bachelor", "master", "phd",
        "computer science", "engineering",
        "information technology"
    ]

    education = []
    for keyword in education_keywords:
        if keyword in text:
            education.append(keyword)

    return list(set(education))
