"""
weights.py
-----------
أوزان مكونات المطابقة في نظام Smart Recruitment AI.

يمكن تعديل هذه القيم حسب:
- طبيعة الوظيفة
- سياسة الشركة
- نتائج التجارب
"""

SCORE_WEIGHTS = {
    "semantic": 0.4,
    "skills": 0.3,
    "title": 0.2,
    "experience": 0.1
}
