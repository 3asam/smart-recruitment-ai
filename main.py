"""
main.py
-------
نقطة التشغيل الرئيسية لمشروع Smart Recruitment AI.

يقوم بـ:
- تحميل بيانات CV و Job Description (كمثال)
- تشغيل محرك المطابقة الذكي
- إخراج النتيجة النهائية بشكل واضح

هذا هو الملف الوحيد الذي يتم تشغيله (Run).
"""

from app.matching.final_score import calculate_final_score


def main():
    """
    مثال تشغيل كامل للنظام.
    في الواقع يمكن استبدال هذه البيانات بمدخلات من:
    - API
    - Database
    - Frontend
    """

    # ----------------------
    # Sample CV Data
    # ----------------------
    cv_data = {
        "skills": [
            "Python",
            "Django",
            "REST APIs",
            "PostgreSQL",
            "Docker"
        ],
        "title": "Backend Developer",
        "years_experience": 5
    }

    # ----------------------
    # Sample Job Description Data
    # ----------------------
    jd_data = {
        "skills": [
            "Python",
            "Django",
            "Docker",
            "AWS"
        ],
        "title": "Senior Backend Engineer",
        "min_years_experience": 4,
        "max_years_experience": 7
    }

    # ----------------------
    # Run Smart Matching Engine
    # ----------------------
    result = calculate_final_score(cv_data=cv_data, jd_data=jd_data)

    # ----------------------
    # Output Result
    # ----------------------
    print("\n====== Smart Recruitment Result ======")
    print(f"Final Score : {result.final_score}")
    print(f"Decision    : {result.decision}\n")

    print("-- Skills Matching --")
    print(result.skills.to_dict())

    print("\n-- Title Matching --")
    print(result.title.to_dict())

    print("\n-- Experience Matching --")
    print(result.experience.to_dict())


if __name__ == "__main__":
    main()
