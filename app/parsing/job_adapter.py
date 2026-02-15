from typing import Dict, List, Union


def build_job_text(job_input: Union[str, Dict]) -> str:
    """
    Adapter ذكي:
    - يقبل Job Description كنص (للتست و Swagger)
    - أو يقبل Job Data كـ dict (من HR / Backend)
    - ويرجع Job Text موحّد للـ Semantic Matching
    """

    # 🟢 لو جاله نص مباشر (Swagger / Candidate test)
    if isinstance(job_input, str):
        return job_input.strip()

    # 🟢 لو جاله dict (HR / Backend)
    if not isinstance(job_input, dict):
        raise ValueError("Job input must be string or dict")

    sections: List[str] = []

    if job_input.get("title"):
        sections.append(f"Job Title: {job_input['title']}")

    if job_input.get("description"):
        sections.append(job_input["description"])

    if job_input.get("skills"):
        sections.append(
            "Required Skills: " + ", ".join(job_input["skills"])
        )

    if job_input.get("responsibilities"):
        if isinstance(job_input["responsibilities"], list):
            sections.append(
                "Responsibilities: " + " ".join(job_input["responsibilities"])
            )
        else:
            sections.append(str(job_input["responsibilities"]))

    if job_input.get("min_years_experience"):
        sections.append(
            f"Minimum {job_input['min_years_experience']} years of experience required"
        )

    if job_input.get("max_years_experience"):
        sections.append(
            f"Maximum {job_input['max_years_experience']} years of experience"
        )

    return "\n".join(sections)
