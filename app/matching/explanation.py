# app/matching/explanation.py

from typing import List


def generate_explanation(
    match_score: float,
    decision: str,
    missing_skills: List[str]
) -> str:
    """
    Generates human-readable explanation for the decision.
    """

    if decision == "ACCEPT":
        level_text = "strong match"
    elif decision == "PENDING":
        level_text = "moderate match"
    else:
        level_text = "weak match"

    explanation = f"The candidate is a {level_text} for this role."

    if missing_skills:
        explanation += f" Missing skills: {', '.join(missing_skills)}."

    return explanation
