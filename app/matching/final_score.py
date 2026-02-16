from typing import Dict, List

from app.matching.semantic import semantic_sentence_matching
from app.matching.skills import match_skills, SkillMatchResult
from app.matching.title import match_title, TitleMatchResult
from app.matching.experience import match_experience, ExperienceMatchResult
from app.matching.missing import get_missing_skills
from app.matching.explanation import generate_explanation

from app.config.weights import SCORE_WEIGHTS
from app.config.thresholds import DECISION_THRESHOLDS


class FinalMatchResult:
    def __init__(
        self,
        final_score: float,
        decision: str,
        semantic_score: float,
        semantic_explainability: List[Dict],
        skills: SkillMatchResult,
        title: TitleMatchResult,
        experience: ExperienceMatchResult,
        missing_skills: List[str],
        explanation: str
    ):
        # Raw score (0 → 1)
        self.raw_score = round(final_score, 3)

        # Percentage score (0 → 100)
        self.match_score = round(final_score * 100, 2)

        self.semantic_score = round(semantic_score, 3)
        self.semantic_explainability = semantic_explainability
        self.decision = decision
        self.skills = skills
        self.title = title
        self.experience = experience
        self.missing_skills = missing_skills
        self.explanation = explanation

    def to_dict(self) -> Dict:
        return {
            "match_score": self.match_score,
            "decision": self.decision,
            "missing_skills": self.missing_skills,
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


def calculate_final_score(
    cv_text: str,
    job_text: str,
    job_data: Dict,
    parsed_cv: Dict
) -> FinalMatchResult:

    # ------------------------------
    # 1️⃣ Semantic Matching
    # ------------------------------
    semantic_result = semantic_sentence_matching(
        cv_text=cv_text,
        job_text=job_text,
        top_k=3
    )

    semantic_score = semantic_result["score"]
    semantic_explainability = semantic_result["top_matches"]

    # ------------------------------
    # 2️⃣ Skill Matching
    # ------------------------------
    skills_result = match_skills(
        cv_skills=parsed_cv.get("skills", []),
        jd_skills=job_data.get("skills", [])
    )

    # ------------------------------
    # 3️⃣ Title Matching
    # ------------------------------
    title_result = match_title(
        cv_title=parsed_cv.get("title", ""),
        jd_title=job_data.get("title", "")
    )

    # ------------------------------
    # 4️⃣ Experience Matching
    # ------------------------------
    experience_result = match_experience(
        cv_years=parsed_cv.get("years_experience", 0),
        jd_min_years=job_data.get("min_years_experience", 0),
        jd_max_years=job_data.get("max_years_experience")
    )

    # ------------------------------
    # 5️⃣ Final Weighted Score
    # ------------------------------
    final_score = (
        semantic_score * SCORE_WEIGHTS["semantic"] +
        skills_result.score * SCORE_WEIGHTS["skills"] +
        title_result.score * SCORE_WEIGHTS["title"] +
        experience_result.score * SCORE_WEIGHTS["experience"]
    )

    final_score = round(final_score, 3)

    # ------------------------------
    # 6️⃣ Decision Logic
    # ------------------------------
    if final_score >= DECISION_THRESHOLDS["accept"]:
        decision = "ACCEPT"
    elif final_score >= DECISION_THRESHOLDS["pending"]:
        decision = "PENDING"
    else:
        decision = "REJECT"

    # ------------------------------
    # 7️⃣ Missing Skills
    # ------------------------------
    missing_skills = get_missing_skills(
        candidate_skills=parsed_cv.get("skills", []),
        job_skills=job_data.get("skills", [])
    )

    # ------------------------------
    # 8️⃣ Explanation
    # ------------------------------
    explanation = generate_explanation(
        match_score=final_score * 100,
        decision=decision,
        missing_skills=missing_skills
    )

    # ------------------------------
    # 9️⃣ Return Structured Result
    # ------------------------------
    return FinalMatchResult(
        final_score=final_score,
        semantic_score=semantic_score,
        semantic_explainability=semantic_explainability,
        decision=decision,
        skills=skills_result,
        title=title_result,
        experience=experience_result,
        missing_skills=missing_skills,
        explanation=explanation
    )
