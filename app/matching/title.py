"""
title.py
--------
مطابقة المسمى الوظيفي (Job Title) بين CV و Job Description
باستخدام Semantic Similarity عبر SBERT.

أهمية هذا الجزء:
- التأكد أن تخصص المرشح قريب من الدور المطلوب
- تقليل الترشيحات غير المناسبة (مثال: Data Analyst vs Backend Developer)
"""

from typing import Dict
import torch
from torch.nn.functional import cosine_similarity

from app.core.embeddings import get_embedding


class TitleMatchResult:
    def __init__(self, score: float):
        self.score = round(score, 3)

    def to_dict(self) -> Dict:
        return {
            "score": self.score
        }


def match_title(
    cv_title: str,
    jd_title: str
) -> TitleMatchResult:
    """
    مطابقة المسمى الوظيفي بين CV و JD.

    Parameters:
        cv_title (str): المسمى الوظيفي في السيرة الذاتية
        jd_title (str): المسمى الوظيفي المطلوب في الوظيفة

    Returns:
        TitleMatchResult
    """

    if not cv_title or not jd_title:
        return TitleMatchResult(0.0)

    cv_emb = get_embedding(cv_title)
    jd_emb = get_embedding(jd_title)

    similarity = cosine_similarity(
        cv_emb.unsqueeze(0),
        jd_emb.unsqueeze(0)
    ).item()

    return TitleMatchResult(similarity)
