from typing import Dict


class ExperienceMatchResult:

    def __init__(self, score: float, delta_years: float):

        self.score = round(score, 3)
        self.delta_years = round(delta_years, 2)

    def to_dict(self) -> Dict:

        return {
            "score": round(self.score * 100, 2),
            "delta_years": self.delta_years
        }


def match_experience(
    cv_years: float,
    jd_min_years: float,
    jd_max_years: float | None = None
):

    cv_years = float(cv_years or 0)
    jd_min_years = float(jd_min_years or 0)

    if jd_max_years is not None:
        jd_max_years = float(jd_max_years)

    delta = cv_years - jd_min_years

    # =====================================
    # 🔴 Case 1: أقل من المطلوب
    # =====================================
    if jd_min_years > 0 and cv_years < jd_min_years:

        # نسبة التغطية
        score = cv_years / jd_min_years

        # penalize شوية
        score *= 0.8

    # =====================================
    # 🟢 Case 2: في الرينج المناسب
    # =====================================
    elif jd_max_years is None or cv_years <= jd_max_years:

        # الأفضل يكون قريب من الحد الأدنى
        if jd_min_years > 0:
            ratio = cv_years / jd_min_years

            # sweet spot
            if 1 <= ratio <= 1.5:
                score = 1.0
            elif ratio <= 2:
                score = 0.9
            else:
                score = 0.85
        else:
            score = 1.0

    # =====================================
    # 🟡 Case 3: Overqualified
    # =====================================
    else:

        extra_years = cv_years - jd_max_years

        # penalty أقوى شوية
        penalty = extra_years * 0.05

        score = max(0.6, 1 - penalty)

    return ExperienceMatchResult(score, delta)
