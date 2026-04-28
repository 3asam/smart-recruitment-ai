from typing import Dict
from app.matching.semantic import semantic_sentence_matching
from app.matching.skills import match_skills
from app.matching.title import match_title
from app.matching.experience import match_experience
from app.matching.explanation import generate_explanation
from app.config.weights import SCORE_WEIGHTS
from app.config.thresholds import DECISION_THRESHOLDS


# ==========================================
# Result Object
# ==========================================
class FinalMatchResult:

    def __init__(
        self,
        final_score,
        decision,
        semantic_score,
        semantic_explainability,
        skills,
        title,
        experience,
        explanation,
        cv_id=None
    ):

        self.cv_id = cv_id

        final_score = max(0.0, min(1.0, final_score))

        self.raw_score = round(final_score * 100, 2)
        self.match_score = self.raw_score
        self.semantic_score = round(semantic_score * 100, 2)

        self.semantic_explainability = semantic_explainability
        self.decision = decision
        self.skills = skills
        self.title = title
        self.experience = experience
        self.explanation = explanation

        self.rank = None  # 🔥 مهم


    def to_dict(self):

        return {
            "cv_id": self.cv_id,
            "rank": self.rank,

            "match_score": self.match_score,
            "decision": self.decision,

            "skills": {
                "matched": self.skills.matched_skills,
                "missing": self.skills.missing_skills
            },

            "explanation": self.explanation,

            "details": {
                "raw_score": self.raw_score,
                "semantic_score": self.semantic_score,
                "semantic_explainability": self.semantic_explainability,
                "skills": self.skills.to_dict(),
                "title": self.title.to_dict(),
                "experience": self.experience.to_dict()
            }
        }


# ==========================================
# Safe Score
# ==========================================
def safe_score(value):
    try:
        return max(0.0, min(1.0, float(value)))
    except:
        return 0.0


# ==========================================
# Final Score Calculation
# ==========================================
def calculate_final_score(
    cv_text: str,
    job_text: str,
    job_data: Dict,
    parsed_cv: Dict,
    cv_id: str = None
):

    # ===============================
    # Semantic
    # ===============================
    semantic_result = semantic_sentence_matching(
        cv_text,
        job_text,
        top_k=3
    )

    semantic_score = safe_score(semantic_result.get("score", 0))
    semantic_explainability = semantic_result.get("top_matches", [])

    # ===============================
    # Skills
    # ===============================
    skills_result = match_skills(
        parsed_cv.get("skills", []),
        job_data.get("skills", [])
    )

    skills_score = safe_score(skills_result.score)

    # ===============================
    # Title
    # ===============================
    title_result = match_title(
        parsed_cv.get("title", ""),
        job_data.get("title", "")
    )

    title_score = safe_score(title_result.score)

    # 🔥 Dynamic fallback
    if title_score == 0:
        if skills_score > 0.7:
            title_score = 0.5
        else:
            title_score = 0.2

    # ===============================
    # Experience
    # ===============================
    experience_result = match_experience(
        parsed_cv.get("experience", 0),
        job_data.get("min_years_experience", 0),
        job_data.get("max_years_experience")
    )

    experience_score = safe_score(experience_result.score)

    # ===============================
    # Final Score
    # ===============================
    final_score = (
        semantic_score * SCORE_WEIGHTS["semantic"] +
        skills_score * SCORE_WEIGHTS["skills"] +
        title_score * SCORE_WEIGHTS["title"] +
        experience_score * SCORE_WEIGHTS["experience"]
    )

    final_score = safe_score(final_score)

    # ===============================
    # Decision
    # ===============================
    if final_score >= DECISION_THRESHOLDS["accept"]:
        decision = "ACCEPT"
    elif final_score >= DECISION_THRESHOLDS["pending"]:
        decision = "PENDING"
    else:
        decision = "REJECT"

    # ===============================
    # Explanation (🔥 FIXED)
    # ===============================
    explanation = generate_explanation(
        match_score=final_score * 100,
        decision=decision,
        missing_skills=skills_result.missing_skills,
        semantic_score=semantic_score,
        title_score=title_score,
        experience_score=experience_score
    )

    # ===============================
    # Return
    # ===============================
    return FinalMatchResult(
        final_score,
        decision,
        semantic_score,
        semantic_explainability,
        skills_result,
        title_result,
        experience_result,
        explanation,
        cv_id=cv_id
    )
