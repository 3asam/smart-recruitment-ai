from typing import List, Dict
from app.matching.final_score import calculate_final_score, FinalMatchResult


def rank_candidates(
    parsed_cvs: List[Dict],
    job_text: str,
    job_data: Dict
) -> List[FinalMatchResult]:
    """
    Rank multiple candidates based on match_score (descending).
    """

    results: List[FinalMatchResult] = []

    for parsed_cv in parsed_cvs:

        # ===============================
        # Extract Data
        # ===============================
        cv_text = parsed_cv.get("cv_text", "")
        cv_id = parsed_cv.get("cv_id")

        # ===============================
        # Safety Check (important 🔥)
        # ===============================
        if not cv_id:
            raise ValueError("cv_id is missing for one of the candidates")

        # ===============================
        # Calculate Score
        # ===============================
        result = calculate_final_score(
            cv_text=cv_text,
            job_text=job_text,
            job_data=job_data,
            parsed_cv=parsed_cv,
            cv_id=cv_id
        )

        results.append(result)

    # ===============================
    # Sort by Highest Score
    # ===============================
    ranked_results = sorted(
        results,
        key=lambda x: x.match_score,
        reverse=True
    )

    return ranked_results
