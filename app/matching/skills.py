"""
skills.py
---------
محرك مطابقة المهارات بين CV و Job Description باستخدام
Semantic Similarity (SBERT + Cosine Similarity).

الهدف:
- حساب Skill Match Score واقعي
- التعامل مع نقص / زيادة المهارات
- إخراج نتيجة قابلة للتفسير
"""

from typing import List, Dict
import torch
from torch.nn.functional import cosine_similarity

from app.core.embeddings import get_embedding, mean_pool_embeddings


class SkillMatchResult:
    def __init__(
        self,
        score: float,
        matched_skills: List[str],
        missing_skills: List[str]
    ):
        self.score = round(score, 3)
        self.matched_skills = matched_skills
        self.missing_skills = missing_skills

    def to_dict(self) -> Dict:
        return {
            "score": self.score,
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
        }


def match_skills(
    cv_skills: List[str],
    jd_skills: List[str],
    threshold: float = 0.7
) -> SkillMatchResult:
    """
    مطابقة مهارات الـ CV مع مهارات الـ JD.

    Parameters:
        cv_skills (List[str]): مهارات المرشح
        jd_skills (List[str]): المهارات المطلوبة
        threshold (float): أقل Cosine Similarity للاعتبار أن المهارة متطابقة

    Returns:
        SkillMatchResult
    """

    if not cv_skills or not jd_skills:
        return SkillMatchResult(0.0, [], jd_skills)

    cv_embeddings = get_embedding(cv_skills)
    jd_embeddings = get_embedding(jd_skills)

    matched = []
    missing = []
    similarity_scores = []

    for jd_skill, jd_emb in zip(jd_skills, jd_embeddings):
        similarities = cosine_similarity(jd_emb.unsqueeze(0), cv_embeddings)
        max_sim = similarities.max().item()

        if max_sim >= threshold:
            matched.append(jd_skill)
            similarity_scores.append(max_sim)
        else:
            missing.append(jd_skill)

    if similarity_scores:
        final_score = sum(similarity_scores) / len(jd_skills)
    else:
        final_score = 0.0

    return SkillMatchResult(final_score, matched, missing)
