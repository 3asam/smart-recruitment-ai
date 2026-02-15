"""
embeddings.py
-------------
هذا الملف مسؤول عن تحويل أي نص (CV / JD / Skills / Title ...)
إلى Embedding Vector باستخدام موديل SBERT المحمّل من model_loader.

⚠️ لا يحتوي على أي منطق Matching أو Scoring
⚠️ مجرد طبقة وسيطة بين النص والموديل
"""

from typing import List, Union, Tuple
import re
import torch

from app.core.model_loader import load_model


TextInput = Union[str, List[str]]


def get_embedding(text: TextInput, normalize: bool = True) -> torch.Tensor:
    """
    تحويل نص واحد أو قائمة نصوص إلى Embedding.

    Parameters:
        text (str | List[str]): النص أو النصوص المطلوب تحويلها
        normalize (bool): هل يتم عمل L2 normalization (مهم لـ cosine similarity)

    Returns:
        torch.Tensor:
            - shape (384,) لنص واحد
            - shape (N, 384) لقائمة نصوص
    """

    model = load_model()

    embedding = model.encode(
        text,
        convert_to_tensor=True,
        normalize_embeddings=normalize
    )

    return embedding


def mean_pool_embeddings(texts: List[str]) -> torch.Tensor:
    """
    حساب embedding متوسط لمجموعة نصوص.
    مفيد في:
    - Skills متعددة
    - Responsibilities متعددة

    Example:
        ["Python", "Django", "REST APIs"]
        → Embedding واحد يمثلهم
    """

    embeddings = get_embedding(texts)

    if embeddings.dim() == 1:
        return embeddings

    return embeddings.mean(dim=0)


# ------------------------------------------------------------------
# Sentence-level preparation (for Semantic Explainability)
# ------------------------------------------------------------------

def split_into_sentences(text: str, min_length: int = 20) -> List[str]:
    """
    تقسيم النص إلى جمل صالحة للاستخدام في التحليل الدلالي.

    Parameters:
        text (str): النص الكامل (CV أو JD)
        min_length (int): أقل طول للجملة المقبولة

    Returns:
        List[str]: قائمة جمل نظيفة
    """
    if not text:
        return []

    raw_sentences = re.split(r"[.\n;]", text)

    return [
        sentence.strip()
        for sentence in raw_sentences
        if len(sentence.strip()) >= min_length
    ]


def get_sentence_embeddings(
    text: str,
    normalize: bool = True
) -> Tuple[List[str], torch.Tensor]:
    """
    تحويل نص كامل إلى:
    - قائمة جمل
    - Embedding لكل جملة

    ⚠️ لا يحتوي على أي similarity أو matching logic

    Returns:
        Tuple:
            - List[str]: الجمل
            - torch.Tensor: embeddings (N, 384)
    """

    sentences = split_into_sentences(text)

    if not sentences:
        return [], torch.empty(0)

    embeddings = get_embedding(sentences, normalize=normalize)

    return sentences, embeddings
