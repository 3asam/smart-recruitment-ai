from fastapi import FastAPI, UploadFile, File, Form
import tempfile
import shutil
import os

from app.parsing.cv_parser.parser import extract_cv_data
from app.parsing.adapter import build_cv_text
from app.parsing.job_adapter import build_job_text
from app.matching.final_score import calculate_final_score

app = FastAPI(
    title="Smart Recruitment AI Service",
    version="3.0"
)

# ==========================================
# 1️⃣ Parse CV Endpoint
# ==========================================
@app.post("/api/ai/parse-cv")
async def parse_cv_endpoint(
    cv: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(cv.file, tmp)
        tmp_path = tmp.name

    try:
        parsed_cv = extract_cv_data(tmp_path)
        return parsed_cv

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# 2️⃣ Match Job Endpoint (ATS Core)
# ==========================================
@app.post("/api/ai/match-job")
async def match_job_endpoint(
    cv: UploadFile = File(...),
    job_description: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(cv.file, tmp)
        tmp_path = tmp.name

    try:
        # 1️⃣ Parse CV
        parsed_cv = extract_cv_data(tmp_path)

        # 2️⃣ Build CV Text
        cv_text = build_cv_text(parsed_cv)

        # 3️⃣ Build Job Text
        job_data = {
            "description": job_description
        }
        job_text = build_job_text(job_data)

        # 4️⃣ Run ATS Engine
        result = calculate_final_score(
            cv_text=cv_text,
            job_text=job_text,
            job_data=job_data,
            parsed_cv=parsed_cv
        )

        # 5️⃣ Return Result (جاهز كنسبة مئوية)
        return result.to_dict()

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
