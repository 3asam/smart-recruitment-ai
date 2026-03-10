def build_cv_text(parsed_cv: dict):

    sections=[]

    if parsed_cv.get("name"):

        sections.append(f"Candidate Name: {parsed_cv['name']}")

    if parsed_cv.get("skills"):

        sections.append("Candidate Skills: "+", ".join(parsed_cv["skills"]))

    if parsed_cv.get("experience"):

        sections.append(f"Total Experience: {parsed_cv['experience']} years")

    if parsed_cv.get("education"):

        sections.append(f"Education: {parsed_cv['education']}")

    return "\n".join(sections)
