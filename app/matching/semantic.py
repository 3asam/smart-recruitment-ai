from typing import Dict, List
import torch
from sentence_transformers import util

from app.core.embeddings import get_sentence_embeddings


# ==========================================
# 🔥 Filter Important Sentences
# ==========================================

def filter_sentences(sentences: List[str]) -> List[str]:

    important = []

    for s in sentences:
        s_lower = s.lower()

        # ❌ استبعد noise
        if any(keyword in s_lower for keyword in [
            "name", "email", "phone", "contact"
        ]):
            continue

        # ✔️ خليك في الجمل المهمة
        if any(keyword in s_lower for keyword in [
            "skill", "experience", "project", "work", "develop"
        ]):
            important.append(s)
        else:
            important.append(s)  # fallback (مش بنرميها خالص)

    return important


# ==========================================
# Semantic Matching
# ==========================================

def semantic_sentence_matching(
    cv_text: str,
    job_text: str,
    top_k: int = 3
) -> Dict:

    cv_sentences, cv_embeddings = get_sentence_embeddings(cv_text)
    jd_sentences, jd_embeddings = get_sentence_embeddings(job_text)

    if len(cv_sentences) == 0 or len(jd_sentences) == 0:
        return {"score": 0.0, "top_matches": []}

    # 🔥 فلترة الجمل
    cv_sentences = filter_sentences(cv_sentences)
    jd_sentences = filter_sentences(jd_sentences)

    # embeddings تاني بعد الفلترة
    cv_sentences, cv_embeddings = get_sentence_embeddings(" ".join(cv_sentences))
    jd_sentences, jd_embeddings = get_sentence_embeddings(" ".join(jd_sentences))

    # similarity matrix
    similarity_matrix = util.cos_sim(cv_embeddings, jd_embeddings)

    matches: List[Dict] = []

    # لكل جملة CV → أحسن JD
    for cv_idx, cv_sentence in enumerate(cv_sentences):

        best_jd_idx = torch.argmax(similarity_matrix[cv_idx]).item()
        score = similarity_matrix[cv_idx][best_jd_idx].item()

        matches.append({
            "cv_sentence": cv_sentence,
            "jd_sentence": jd_sentences[best_jd_idx],
            "score": round(score, 3)
        })

    # ترتيب
    matches.sort(key=lambda x: x["score"], reverse=True)

    # ==========================================
    # 🔥 Improved Semantic Score
    # ==========================================

    # ناخد أفضل matches فقط بدل المتوسط العام
    top_scores = [m["score"] for m in matches[:top_k]]

    if top_scores:
        semantic_score = sum(top_scores) / len(top_scores)
    else:
        semantic_score = 0.0

    return {
        "score": round(semantic_score, 3),
        "top_matches": matches[:top_k]
    }


# ==========================================
# Simple Match
# ==========================================

def semantic_match(
    cv_text: str,
    job_text: str
) -> float:

    result = semantic_sentence_matching(
        cv_text=cv_text,
        job_text=job_text,
        top_k=1
    )

    return result["score"]
