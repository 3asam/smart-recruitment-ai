"""
semantic.py
-----------
مسؤول عن:
- Semantic Matching بين CV و Job Description
- Sentence-level similarity
- Top-N matches لشرح سبب الـ semantic score

يعتمد على:
- embeddings.py (تحضير الجمل + embeddings)
- cosine similarity (هنا فقط)
"""

from typing import Dict, List
import torch
from sentence_transformers import util

from app.core.embeddings import get_sentence_embeddings


def semantic_sentence_matching(
    cv_text: str,
    job_text: str,
    top_k: int = 3
) -> Dict:
    """
    Semantic matching على مستوى الجمل مع Explainability.

    Returns:
        {
            "score": float,
            "top_matches": [
                {
                    "cv_sentence": str,
                    "jd_sentence": str,
                    "score": float
                }
            ]
        }
    """

    # --- Prepare sentence embeddings ---
    cv_sentences, cv_embeddings = get_sentence_embeddings(cv_text)
    jd_sentences, jd_embeddings = get_sentence_embeddings(job_text)

    if len(cv_sentences) == 0 or len(jd_sentences) == 0:
        return {
            "score": 0.0,
            "top_matches": []
        }

    # --- Cosine similarity matrix ---
    similarity_matrix = util.cos_sim(cv_embeddings, jd_embeddings)

    matches: List[Dict] = []

    # لكل جملة CV نجيب أحسن جملة JD
    for cv_idx, cv_sentence in enumerate(cv_sentences):
        best_jd_idx = torch.argmax(similarity_matrix[cv_idx]).item()
        score = similarity_matrix[cv_idx][best_jd_idx].item()

        matches.append({
            "cv_sentence": cv_sentence,
            "jd_sentence": jd_sentences[best_jd_idx],
            "score": round(score, 3)
        })

    # --- ترتيب النتائج ---
    matches.sort(key=lambda x: x["score"], reverse=True)

    # --- Semantic score العام ---
    semantic_score = float(similarity_matrix.mean().item())

    return {
        "score": round(semantic_score, 3),
        "top_matches": matches[:top_k]
    }


def semantic_match(
    cv_text: str,
    job_text: str
) -> float:
    """
    Simple semantic score فقط (بدون explainability)
    مفيد في حالات محتاجين score سريع.
    """

    result = semantic_sentence_matching(
        cv_text=cv_text,
        job_text=job_text,
        top_k=1
    )

    return result["score"]
