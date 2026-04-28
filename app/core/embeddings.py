from typing import List, Union, Tuple
import re
import torch

from app.core.model_loader import load_model


TextInput = Union[str, List[str]]


# ==========================================
# 🔥 FIXED: Always return 2D embeddings
# ==========================================
def get_embedding(text: TextInput, normalize: bool = True) -> torch.Tensor:

    model = load_model()

    embedding = model.encode(
        text,
        convert_to_tensor=True,
        normalize_embeddings=normalize
    )

    # 🔥 الحل الأساسي
    if embedding.dim() == 1:
        embedding = embedding.unsqueeze(0)

    return embedding


# ==========================================
# Mean Pooling
# ==========================================
def mean_pool_embeddings(texts: List[str]) -> torch.Tensor:

    embeddings = get_embedding(texts)

    return embeddings.mean(dim=0)


# ==========================================
# Sentence Splitting
# ==========================================
def split_into_sentences(text: str, min_length: int = 20) -> List[str]:

    if not text:
        return []

    raw_sentences = re.split(r"[.\n;]", text)

    return [
        sentence.strip()
        for sentence in raw_sentences
        if len(sentence.strip()) >= min_length
    ]


# ==========================================
# Sentence Embeddings
# ==========================================
def get_sentence_embeddings(
    text: str,
    normalize: bool = True
) -> Tuple[List[str], torch.Tensor]:

    sentences = split_into_sentences(text)

    if not sentences:
        return [], torch.empty((0, 384))

    embeddings = get_embedding(sentences, normalize=normalize)

    return sentences, embeddings
