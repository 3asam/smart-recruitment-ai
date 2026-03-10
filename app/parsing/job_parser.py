import re
from typing import Dict, List


SKILLS = [
 "python","sql","java","git","docker",
 "api","machine learning","data analysis"
]


def parse_job_description(text: str) -> Dict:

 text_lower = text.lower()

 skills = []

 for skill in SKILLS:

  if re.search(r"\b" + skill + r"\b", text_lower):

   skills.append(skill)

 return {
  "description": text,
  "skills": skills,
  "title": "",
  "min_years_experience": 0
 }
