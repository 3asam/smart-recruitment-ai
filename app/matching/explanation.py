from typing import List


def generate_explanation(
    match_score: float,
    decision: str,
    missing_skills: List[str],
    semantic_score: float = None,
    title_score: float = None,
    experience_score: float = None
) -> str:
    """
    Generates smart human-readable explanation.
    """

    # ==========================================
    # Match Level
    # ==========================================
    if decision == "ACCEPT":
        level_text = "strong match"
    elif decision == "PENDING":
        level_text = "moderate match"
    else:
        level_text = "weak match"

    explanation_parts = [
        f"The candidate is a {level_text} for this role."
    ]

    # ==========================================
    # Skills Analysis
    # ==========================================
    if missing_skills:
        explanation_parts.append(
            f"Missing key skills: {', '.join(missing_skills)}."
        )
    else:
        explanation_parts.append(
            "The candidate meets the required skills."
        )

    # ==========================================
    # Semantic Insight
    # ==========================================
    if semantic_score is not None:
        if semantic_score < 0.3:
            explanation_parts.append(
                "The CV content shows low relevance to the job description."
            )
        elif semantic_score < 0.6:
            explanation_parts.append(
                "The CV is somewhat aligned with the job requirements."
            )
        else:
            explanation_parts.append(
                "The CV is highly aligned with the job requirements."
            )

    # ==========================================
    # Title Matching
    # ==========================================
    if title_score is not None:
        if title_score < 0.3:
            explanation_parts.append(
                "The candidate's job title does not closely match the role."
            )
        elif title_score < 0.7:
            explanation_parts.append(
                "The candidate's job title partially matches the role."
            )
        else:
            explanation_parts.append(
                "The candidate's job title strongly matches the role."
            )

    # ==========================================
    # Experience Matching
    # ==========================================
    if experience_score is not None:
        if experience_score < 0.5:
            explanation_parts.append(
                "The candidate has less experience than required."
            )
        elif experience_score < 0.9:
            explanation_parts.append(
                "The candidate has acceptable experience."
            )
        else:
            explanation_parts.append(
                "The candidate's experience level is well suited for the role."
            )

    return " ".join(explanation_parts)
