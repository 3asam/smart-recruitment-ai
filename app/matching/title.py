from typing import Dict
from torch.nn.functional import cosine_similarity
from app.core.embeddings import get_embedding
import re


class TitleMatchResult:

    def __init__(self, score: float):
        self.score = round(score, 3)

    def to_dict(self) -> Dict:
        return {
            "score": round(self.score * 100, 2)
        }


def ensure_2d(tensor):
    if len(tensor.shape) == 1:
        return tensor.unsqueeze(0)
    return tensor


def normalize_title(title: str) -> str:

    title = title.lower()

    title = title.replace("back-end", "backend")
    title = title.replace("front-end", "frontend")
    title = title.replace(".net", "dotnet")

    title = re.sub(r"[^a-z0-9\s]", " ", title)
    title = re.sub(r"\s+", " ", title)

    return title.strip()


IMPORTANT_WORDS = [
    "backend", "frontend", "data", "engineer",
    "developer", "analyst", "scientist",
    "dotnet", "python", "java"
]


def match_title(cv_title: str, jd_title: str):

    if not cv_title or not jd_title:
        return TitleMatchResult(0.0)

    cv_title = normalize_title(cv_title)
    jd_title = normalize_title(jd_title)

    # Exact match
    if cv_title == jd_title:
        return TitleMatchResult(1.0)

    # Word overlap (weighted)
    cv_words = set(cv_title.split())
    jd_words = set(jd_title.split())

    weighted_total = 0
    weighted_overlap = 0

    for word in jd_words:

        weight = 2 if word in IMPORTANT_WORDS else 1

        weighted_total += weight

        if word in cv_words:
            weighted_overlap += weight

    overlap_score = weighted_overlap / weighted_total if weighted_total else 0

    # Semantic
    cv_emb = ensure_2d(get_embedding(cv_title))
    jd_emb = ensure_2d(get_embedding(jd_title))

    semantic_score = cosine_similarity(cv_emb, jd_emb).item()
    semantic_score = max(0.0, min(semantic_score, 1.0))

    # Final
    final_score = (overlap_score * 0.65) + (semantic_score * 0.35)

    return TitleMatchResult(final_score)
