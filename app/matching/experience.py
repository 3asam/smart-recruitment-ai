"""
experience.py
-------------
تقييم توافق الخبرة (سنوات الخبرة) بين المرشح ومتطلبات الوظيفة.

الفكرة:
- الخبرة رقمية وليست نصية
- لا نستخدم NLP هنا
- نحسب Score عادل مع Penalty و Boost
"""

from typing import Dict


class ExperienceMatchResult:
    def __init__(self, score: float, delta_years: float):
        self.score = round(score, 3)
        self.delta_years = delta_years  # الفرق بين خبرة المرشح والمطلوب

    def to_dict(self) -> Dict:
        return {
            "score": self.score,
            "delta_years": self.delta_years
        }


def match_experience(
    cv_years: float,
    jd_min_years: float,
    jd_max_years: float | None = None
) -> ExperienceMatchResult:
    """
    مطابقة سنوات الخبرة.

    Parameters:
        cv_years (float): سنوات خبرة المرشح
        jd_min_years (float): أقل سنوات خبرة مطلوبة
        jd_max_years (float | None): الحد الأقصى (اختياري)

    Returns:
        ExperienceMatchResult
    """

    if cv_years is None or jd_min_years is None:
        return ExperienceMatchResult(0.0, 0.0)

    # الفرق بين خبرة المرشح والحد الأدنى
    delta = cv_years - jd_min_years

    # أقل من المطلوب
    if cv_years < jd_min_years:
        # Penalty تدريجي
        score = max(0.0, cv_years / jd_min_years)

    # داخل النطاق المطلوب
    elif jd_max_years is None or cv_years <= jd_max_years:
        score = 1.0

    # أعلى من المطلوب (Overqualified)
    else:
        # خصم بسيط وليس عقوبة
        score = max(0.7, 1 - ((cv_years - jd_max_years) * 0.05))

    return ExperienceMatchResult(score, delta)
