"""
model_loader.py
----------------
هذا الملف مسؤول عن تحميل موديل الذكاء الاصطناعي (Sentence-BERT)
مرة واحدة فقط، وإعادة استخدامه في جميع أجزاء المشروع.

دوره أساسي كبنية تحتية (AI Infrastructure)
ولا يحتوي على أي منطق Matching أو Business Logic.
"""

from sentence_transformers import SentenceTransformer
import torch

# متغير خاص لحفظ نسخة واحدة من الموديل (Singleton)
_model: SentenceTransformer | None = None


def get_device() -> str:
    """
    تحديد الجهاز المناسب لتشغيل الموديل.
    - GPU (CUDA) إذا كان متاحًا
    - CPU كحل بديل
    """
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    تحميل موديل Sentence-BERT عند أول استدعاء فقط.
    أي استدعاء لاحق سيعيد نفس النسخة المحمّلة مسبقًا.

    Parameters:
        model_name (str): اسم الموديل من sentence-transformers

    Returns:
        SentenceTransformer: نسخة جاهزة للاستخدام من الموديل
    """
    global _model

    if _model is None:
        device = get_device()
        print(f"[model_loader] Loading model '{model_name}' on {device}...")

        _model = SentenceTransformer(
            model_name,
            device=device
        )

        print("[model_loader] Model loaded successfully")

    return _model


# يسمح بتشغيل الملف مباشرة لاختبار التحميل فقط
if __name__ == "__main__":
    model = load_model()
    embedding = model.encode(
        "This is a test sentence",
        convert_to_tensor=True
    )
    print("Test embedding shape:", embedding.shape)
