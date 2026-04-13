# app/matching/ranking.py

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

        cv_text = parsed_cv.get("cv_text", "")

        # ✅ استخرج cv_id من الـ parsed_cv
        cv_id = parsed_cv.get("cv_id")

        result = calculate_final_score(
            cv_text=cv_text,
            job_text=job_text,
            job_data=job_data,
            parsed_cv=parsed_cv,
            cv_id=cv_id  # ✅ التعديل هنا
        )

        results.append(result)

    # Sort by highest match_score (percentage)
    ranked_results = sorted(
        results,
        key=lambda x: x.match_score,
        reverse=True
    )

    return ranked_results
