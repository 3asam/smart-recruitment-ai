from typing import List, Dict
from torch.nn.functional import cosine_similarity
from app.core.embeddings import get_embedding


class SkillMatchResult:

    def __init__(self, score: float, matched_skills: List[str], missing_skills: List[str]):

        self.score = round(score,3)

        self.matched_skills = matched_skills

        self.missing_skills = missing_skills


    def to_dict(self) -> Dict:

        return {
            "score": round(self.score * 100,2),
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills
        }


def match_skills(cv_skills: List[str], jd_skills: List[str], threshold: float = 0.7):

    if not cv_skills or not jd_skills:
        return SkillMatchResult(0.0, [], jd_skills)

    cv_skills = list(set([s.lower() for s in cv_skills]))
    jd_skills = list(set([s.lower() for s in jd_skills]))

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

    if jd_skills:
        coverage_score = len(matched) / len(jd_skills)
    else:
        coverage_score = 0.0

    if similarity_scores:
        semantic_strength = sum(similarity_scores) / len(similarity_scores)
    else:
        semantic_strength = 0.0

    final_score = coverage_score * semantic_strength

    return SkillMatchResult(final_score, matched, missing)
