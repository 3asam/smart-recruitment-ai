import re
from typing import Dict, List


# ==========================================
# Expanded Skill Set (🔥 مهم جدًا)
# ==========================================

COMMON_SKILLS = [
    # Data
    "python", "sql", "excel", "power bi", "tableau",
    "pandas", "numpy", "machine learning", "deep learning",
    "data analysis", "statistics",

    # Backend
    "java", "c++", "c#", ".net", "asp.net",
    "entity framework", "spring", "django", "flask", "fastapi",

    # General
    "git", "docker", "api", "rest api",
    "aws", "azure", "gcp"
]


# ==========================================
# Normalize
# ==========================================

def normalize_text(text: str) -> str:
    return text.lower().strip()


# ==========================================
# Extract Skills (🔥 improved)
# ==========================================

def extract_skills(text: str) -> List[str]:

    text = normalize_text(text)

    found_skills = []

    for skill in COMMON_SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


# ==========================================
# Extract Experience (🔥 improved)
# ==========================================

def extract_experience(text: str) -> int:

    text = normalize_text(text)

    # 1-3 years
    range_match = re.search(r"(\d+)\s*-\s*(\d+)\s*years?", text)
    if range_match:
        return int(range_match.group(1))  # minimum

    # minimum 2 years
    min_match = re.search(r"minimum\s*(\d+)\s*years?", text)
    if min_match:
        return int(min_match.group(1))

    # 2+ years
    plus_match = re.search(r"(\d+)\s*\+\s*years?", text)
    if plus_match:
        return int(plus_match.group(1))

    # fallback
    match = re.search(r"(\d+)\s*years?", text)
    if match:
        return int(match.group(1))

    return 0


# ==========================================
# Extract Title (🔥 smart)
# ==========================================

def extract_title(text: str) -> str:

    lines = text.strip().split("\n")

    for line in lines[:5]:  # أول 5 سطور بس

        clean_line = line.strip()

        if not clean_line:
            continue

        # استبعد جمل مش title
        if any(word in clean_line.lower() for word in ["we are", "looking", "job description"]):
            continue

        # لو السطر قصير → غالبًا title
        if 2 <= len(clean_line.split()) <= 6:
            return clean_line

    return lines[0].strip() if lines else ""


# ==========================================
# Main Parser
# ==========================================

def parse_job_description(text: str) -> Dict:

    skills = extract_skills(text)
    experience = extract_experience(text)
    title = extract_title(text)

    return {
        "description": text,
        "skills": skills,
        "title": title,
        "min_years_experience": experience
    }
