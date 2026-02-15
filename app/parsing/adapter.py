def build_cv_text(parsed_cv: dict) -> str:
    sections = []

    if parsed_cv.get("summary"):
        sections.append(parsed_cv["summary"])

    if parsed_cv.get("skills"):
        sections.append("Skills: " + ", ".join(parsed_cv["skills"]))

    if parsed_cv.get("experience"):
        for exp in parsed_cv["experience"]:
            if isinstance(exp, dict):
                sections.append(
                    f"{exp.get('title', '')} at {exp.get('company', '')}. "
                    f"{exp.get('description', '')}"
                )
            else:
                sections.append(str(exp))

    if parsed_cv.get("education"):
        for edu in parsed_cv["education"]:
            if isinstance(edu, dict):
                sections.append(
                    f"{edu.get('degree', '')} - {edu.get('institution', '')}"
                )
            else:
                sections.append(str(edu))

    return "\n".join(sections)
