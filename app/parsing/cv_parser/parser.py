import re
import pdfplumber
from typing import Dict, List, Optional


# --------------------------------
# Known Skills List
# --------------------------------

SKILLS_LIST = [
    "python",
    "java",
    "c++",
    "sql",
    "javascript",
    "machine learning",
    "deep learning",
    "nlp",
    "pandas",
    "numpy",
    "react",
    "next.js",
    "node.js",
    "c#",
    "mongodb",
    "tailwind",
    "html",
    "css",
    "git",
    "rest apis",
    "api",
    "docker"
]


# --------------------------------
# Main CV Parser
# --------------------------------

def extract_cv_data(file_path: str) -> Dict:

    text = _extract_text_from_pdf(file_path)

    cleaned_text = _clean_text(text)

    return {
        "name": _extract_name(text),
        "email": _extract_email(cleaned_text),
        "phone": _extract_phone(cleaned_text),
        "skills": _extract_skills(cleaned_text),
        "experience": _extract_experience(cleaned_text),
        "education": _extract_education(cleaned_text)
    }


# --------------------------------
# Extract Text from PDF
# --------------------------------

def _extract_text_from_pdf(file_path: str) -> str:

    content = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                content += page_text + "\n"

    return content


# --------------------------------
# Clean Text
# --------------------------------

def _clean_text(text: str) -> str:

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------
# Extract Email
# --------------------------------

def _extract_email(text: str) -> Optional[str]:

    match = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text)

    return match.group(0) if match else None


# --------------------------------
# Extract Phone
# --------------------------------

def _extract_phone(text: str) -> Optional[str]:

    match = re.search(
        r"(\+?\d{1,3})?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}",
        text
    )

    return match.group(0) if match else None


# --------------------------------
# Extract Name
# --------------------------------

def _extract_name(text: str) -> Optional[str]:

    lines = text.split("\n")

    for line in lines[:5]:

        candidate = line.strip()

        if 2 <= len(candidate.split()) <= 4:

            if not any(char.isdigit() for char in candidate):

                return candidate.title()

    return None


# --------------------------------
# Extract Skills
# --------------------------------

def _extract_skills(text: str) -> List[str]:

    found = []

    for skill in SKILLS_LIST:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found.append(skill)

    return sorted(list(set(found)))


# --------------------------------
# Extract Experience
# --------------------------------

def _extract_experience(text: str) -> int:

    patterns = [
        r"(\d+)\s*\+?\s*years",
        r"(\d+)\s*\+?\s*yrs",
        r"(\d+)\s*\+?\s*year"
    ]

    years = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:

            years.append(int(match))

    if years:

        return max(years)

    return 0


# --------------------------------
# Extract Education
# --------------------------------

def _extract_education(text: str) -> Optional[str]:

    text = text.lower()

    degree_keywords = [
        "bachelor",
        "b.sc",
        "bsc",
        "master",
        "msc",
        "phd",
        "doctorate"
    ]

    field_keywords = [
        "computer science",
        "software engineering",
        "information technology",
        "artificial intelligence",
        "computer engineering",
        "data science",
        "information systems",
        "computers and artificial intelligence",
        "computers and information"
    ]

    # search for degree + field
    for degree in degree_keywords:

        if degree in text:

            for field in field_keywords:

                if field in text:

                    return f"{degree.title()} in {field.title()}"

            return degree.title()

    # search for field only
    for field in field_keywords:

        if field in text:

            return field.title()

    # fallback if university detected
    if "faculty" in text or "university" in text:

        return "University Degree"

    return None
