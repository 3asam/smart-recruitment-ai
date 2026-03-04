"""
model_loader.py
----------------
Responsible for loading the Sentence-BERT model once (Singleton pattern)
and reusing it across the entire application.

This module contains no business logic.
"""

from sentence_transformers import SentenceTransformer
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def get_device() -> str:
    """
    Determine best available device.
    Priority:
    1. CUDA (if available)
    2. CPU fallback
    """
    try:
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass

    return "cpu"


def load_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Load SentenceTransformer model once (Singleton).
    """
    global _model

    if _model is None:
        device = get_device()
        logger.info(f"[model_loader] Loading model '{model_name}' on {device}...")

        try:
            _model = SentenceTransformer(
                model_name,
                device=device
            )
            logger.info("[model_loader] Model loaded successfully")

        except Exception as e:
            logger.exception("[model_loader] Failed to load model")
            raise e

    return _model


# Standalone test
if __name__ == "__main__":
    model = load_model()
    embedding = model.encode(
        "This is a test sentence",
        convert_to_tensor=True
    )
    print("Test embedding shape:", embedding.shape)
    