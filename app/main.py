from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import tempfile
import shutil
import os

from app.parsing.cv_parser.parser import extract_cv_data
from app.parsing.adapter import build_cv_text
from app.parsing.job_adapter import build_job_text
from app.matching.final_score import calculate_final_score
from app.matching.ranking import rank_candidates

app = FastAPI(
    title="Smart Recruitment AI Service",
    version="4.0"
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
# 2️⃣ Match Job Endpoint (Single Candidate)
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
        parsed_cv = extract_cv_data(tmp_path)
        cv_text = build_cv_text(parsed_cv)

        job_data = {
            "description": job_description
        }

        job_text = build_job_text(job_data)

        result = calculate_final_score(
            cv_text=cv_text,
            job_text=job_text,
            job_data=job_data,
            parsed_cv=parsed_cv
        )

        return result.to_dict()

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# 3️⃣ Rank Multiple Candidates
# ==========================================
@app.post("/api/ai/rank-candidates")
async def rank_candidates_endpoint(
    cvs: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    parsed_cvs = []

    for cv in cvs:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(cv.file, tmp)
            tmp_path = tmp.name

        try:
            parsed_cv = extract_cv_data(tmp_path)
            cv_text = build_cv_text(parsed_cv)

            parsed_cv["cv_text"] = cv_text
            parsed_cvs.append(parsed_cv)

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    job_data = {
        "description": job_description
    }

    job_text = build_job_text(job_data)

    ranked_results = rank_candidates(
        parsed_cvs=parsed_cvs,
        job_text=job_text,
        job_data=job_data
    )

    return [result.to_dict() for result in ranked_results]
