from typing import Dict,List
from app.matching.semantic import semantic_sentence_matching
from app.matching.skills import match_skills
from app.matching.title import match_title
from app.matching.experience import match_experience
from app.matching.explanation import generate_explanation
from app.config.weights import SCORE_WEIGHTS
from app.config.thresholds import DECISION_THRESHOLDS


class FinalMatchResult:

    def __init__(self,final_score,decision,semantic_score,semantic_explainability,skills,title,experience,explanation):

        self.raw_score = round(final_score*100,2)

        self.match_score = self.raw_score

        self.semantic_score = round(semantic_score*100,2)

        self.semantic_explainability = semantic_explainability

        self.decision = decision

        self.skills = skills

        self.title = title

        self.experience = experience

        self.explanation = explanation


    def to_dict(self):

        return {

            "match_score": self.match_score,

            "decision": self.decision,

            "skills":{

                "matched":self.skills.matched_skills,

                "missing":self.skills.missing_skills

            },

            "explanation":self.explanation,

            "details":{

                "raw_score":self.raw_score,

                "semantic_score":self.semantic_score,

                "semantic_explainability":self.semantic_explainability,

                "skills":self.skills.to_dict(),

                "title":self.title.to_dict(),

                "experience":self.experience.to_dict()

            }
        }


def calculate_final_score(cv_text,job_text,job_data,parsed_cv):

    semantic_result = semantic_sentence_matching(cv_text,job_text,top_k=3)

    semantic_score = semantic_result["score"]

    semantic_explainability = semantic_result["top_matches"]

    skills_result = match_skills(parsed_cv.get("skills",[]),job_data.get("skills",[]))

    title_result = match_title(parsed_cv.get("title",""),job_data.get("title",""))

    experience_result = match_experience(parsed_cv.get("experience",0),job_data.get("min_years_experience",0),job_data.get("max_years_experience"))

    final_score = (

        semantic_score * SCORE_WEIGHTS["semantic"] +

        skills_result.score * SCORE_WEIGHTS["skills"] +

        title_result.score * SCORE_WEIGHTS["title"] +

        experience_result.score * SCORE_WEIGHTS["experience"]

    )

    if final_score >= DECISION_THRESHOLDS["accept"]:

        decision="ACCEPT"

    elif final_score >= DECISION_THRESHOLDS["pending"]:

        decision="PENDING"

    else:

        decision="REJECT"

    explanation = generate_explanation(

        match_score=final_score*100,

        decision=decision,

        missing_skills=skills_result.missing_skills

    )

    return FinalMatchResult(

        final_score,

        decision,

        semantic_score,

        semantic_explainability,

        skills_result,

        title_result,

        experience_result,

        explanation

    )
