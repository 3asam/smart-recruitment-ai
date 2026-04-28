from typing import List, Dict
from app.matching.final_score import calculate_final_score, FinalMatchResult
import uuid


def generate_cv_id(index: int = None) -> str:
    """
    Generate clean CV ID
    """
    if index is not None:
        return f"CV-{str(index).zfill(4)}"
    return f"CV-{str(uuid.uuid4())[:8].upper()}"


def rank_candidates(
    parsed_cvs: List[Dict],
    job_text: str,
    job_data: Dict
) -> List[FinalMatchResult]:

    results: List[FinalMatchResult] = []

    # ======================================
    # Process each CV
    # ======================================
    for idx, parsed_cv in enumerate(parsed_cvs, start=1):

        cv_text = parsed_cv.get("cv_text", "")

        # 🔥 Smart ID handling
        cv_id = parsed_cv.get("cv_id")

        if not cv_id:
            cv_id = generate_cv_id(idx)

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

    # ======================================
    # Sort by score
    # ======================================
    ranked_results = sorted(
        results,
        key=lambda x: x.match_score,
        reverse=True
    )

    # ======================================
    # Assign rank AFTER sorting
    # ======================================
    for rank, res in enumerate(ranked_results, start=1):
        res.rank = rank

    return ranked_results
