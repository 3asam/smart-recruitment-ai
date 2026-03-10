from typing import Dict


class ExperienceMatchResult:

    def __init__(self, score: float, delta_years: float):

        self.score = round(score,3)
        self.delta_years = delta_years


    def to_dict(self) -> Dict:

        return {
            "score": round(self.score * 100,2),
            "delta_years": self.delta_years
        }


def match_experience(cv_years: float, jd_min_years: float, jd_max_years: float | None = None):

    cv_years = float(cv_years or 0)
    jd_min_years = float(jd_min_years or 0)

    if jd_max_years is not None:
        jd_max_years = float(jd_max_years)

    delta = cv_years - jd_min_years

    if jd_min_years > 0 and cv_years < jd_min_years:

        score = cv_years / jd_min_years

    elif jd_max_years is None or cv_years <= jd_max_years:

        score = 1.0

    else:

        extra_years = cv_years - jd_max_years

        penalty = extra_years * 0.03

        score = max(0.75, 1 - penalty)

    return ExperienceMatchResult(score, delta)
