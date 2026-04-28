from typing import List, Dict
from torch.nn.functional import cosine_similarity
from app.core.embeddings import get_embedding


class SkillMatchResult:

    def __init__(self, score: float, matched_skills: List[str], missing_skills: List[str]):

        self.score = round(score, 3)
        self.matched_skills = matched_skills
        self.missing_skills = missing_skills

    def to_dict(self) -> Dict:

        return {
            "score": round(self.score * 100, 2),
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills
        }


IMPORTANT_SKILLS = [
    "python", "sql", "c#", ".net", "java"
]


def ensure_2d(tensor):
    if len(tensor.shape) == 1:
        return tensor.unsqueeze(0)
    return tensor


def match_skills(
    cv_skills: List[str],
    jd_skills: List[str],
    threshold: float = 0.7
):

    if not cv_skills or not jd_skills:
        return SkillMatchResult(0.0, [], jd_skills)

    # Normalize
    cv_skills = list(set([s.lower().strip() for s in cv_skills]))
    jd_skills = list(set([s.lower().strip() for s in jd_skills]))

    # Exact match
    exact_matches = set(cv_skills) & set(jd_skills)

    remaining_jd_skills = [s for s in jd_skills if s not in exact_matches]

    # Embeddings
    cv_embeddings = get_embedding(cv_skills)
    cv_embeddings = ensure_2d(cv_embeddings)

    jd_embeddings = get_embedding(remaining_jd_skills) if remaining_jd_skills else []

    matched = list(exact_matches)
    missing = []
    similarity_scores = []

    # Semantic matching
    for jd_skill, jd_emb in zip(remaining_jd_skills, jd_embeddings):

        jd_emb = ensure_2d(jd_emb)

        similarities = cosine_similarity(jd_emb, cv_embeddings)

        max_sim = similarities.max().item()

        if max_sim >= threshold:
            matched.append(jd_skill)
            similarity_scores.append(max_sim)
        else:
            missing.append(jd_skill)

    # =========================
    # Smart Scoring
    # =========================

    weighted_total = 0
    weighted_matched = 0

    for skill in jd_skills:

        weight = 2 if skill in IMPORTANT_SKILLS else 1

        weighted_total += weight

        if skill in matched:
            weighted_matched += weight

    coverage_score = weighted_matched / weighted_total if weighted_total else 0

    if similarity_scores:
        semantic_strength = sum(similarity_scores) / len(similarity_scores)
    else:
        semantic_strength = 1.0 if exact_matches else 0.0

    final_score = (coverage_score * 0.75) + (semantic_strength * 0.25)

    return SkillMatchResult(final_score, matched, missing)
