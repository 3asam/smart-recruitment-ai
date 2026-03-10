from typing import Dict
from torch.nn.functional import cosine_similarity
from app.core.embeddings import get_embedding


class TitleMatchResult:

    def __init__(self, score: float):

        self.score = round(score,3)


    def to_dict(self) -> Dict:

        return {
            "score": round(self.score * 100,2)
        }


def _clean_title(title: str) -> str:

    return title.lower().strip()


def match_title(cv_title: str, jd_title: str):

    if not cv_title or not jd_title:
        return TitleMatchResult(0.0)

    cv_title = _clean_title(cv_title)
    jd_title = _clean_title(jd_title)

    cv_emb = get_embedding(cv_title)
    jd_emb = get_embedding(jd_title)

    similarity = cosine_similarity(cv_emb, jd_emb).item()

    similarity = max(0.0, min(similarity,1.0))

    return TitleMatchResult(similarity)
