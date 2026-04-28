"""
weights.py
-----------
Dynamic & realistic scoring weights
for Smart Recruitment AI.
"""

# ==========================================
# 🔥 Default Weights (Balanced)
# ==========================================

SCORE_WEIGHTS = {
    "skills": 0.4,        # 🔥 الأهم
    "semantic": 0.3,      # مساعد
    "title": 0.2,         # مهم لتحديد role
    "experience": 0.1     # ضبط نهائي
}
