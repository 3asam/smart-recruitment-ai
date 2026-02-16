# app/matching/missing.py

from typing import List


def get_missing_skills(
    candidate_skills: List[str],
    job_skills: List[str]
) -> List[str]:
    """
    Returns list of missing required skills.
    """

    candidate_set = {s.lower().strip() for s in candidate_skills}
    job_set = {s.lower().strip() for s in job_skills}

    missing = job_set - candidate_set

    return list(missing)
