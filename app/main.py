from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import tempfile
import shutil
import os
import logging

from app.parsing.cv_parser.parser import extract_cv_data
from app.parsing.adapter import build_cv_text
from app.parsing.job_adapter import build_job_text
from app.parsing.job_parser import parse_job_description

from app.matching.final_score import calculate_final_score
from app.matching.ranking import rank_candidates
from app.core.model_loader import load_model


# ==========================================
# Logging Configuration
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==========================================
# FastAPI App Initialization
# ==========================================
app = FastAPI(
    title="Smart Recruitment AI Service",
    version="4.2"
)


# ==========================================
# Startup Event (Load AI Model Once)
# ==========================================
@app.on_event("startup")
def startup_event():
    logger.info("Starting Smart Recruitment AI service...")
    load_model()
    logger.info("AI model loaded at startup.")


# ==========================================
# Health Check Endpoint
# ==========================================
@app.get("/health")
def health():
    return {"status": "ok"}


# ==========================================
# Parse CV Endpoint
# ==========================================
@app.post("/api/ai/parse-cv")
async def parse_cv_endpoint(
    cv: UploadFile = File(...)
):
    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(cv.file, tmp)
            tmp_path = tmp.name

        parsed_cv = extract_cv_data(tmp_path)

        return parsed_cv

    except Exception as e:

        logger.exception("Error while parsing CV")
        raise HTTPException(status_code=400, detail=str(e))

    finally:

        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# Match Job Endpoint (Single Candidate)
# ==========================================
@app.post("/api/ai/match-job")
async def match_job_endpoint(
    cv: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(cv.file, tmp)
            tmp_path = tmp.name

        parsed_cv = extract_cv_data(tmp_path)

        cv_text = build_cv_text(parsed_cv)

        job_data = parse_job_description(job_description)
        job_text = build_job_text(job_data)

        result = calculate_final_score(
            cv_text=cv_text,
            job_text=job_text,
            job_data=job_data,
            parsed_cv=parsed_cv
        )

        return result.to_dict()

    except Exception as e:

        logger.exception("Error during job matching")
        raise HTTPException(status_code=400, detail=str(e))

    finally:

        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# Rank Multiple Candidates
# ==========================================
@app.post("/api/ai/rank-candidates")
async def rank_candidates_endpoint(
    cvs: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    parsed_cvs = []

    try:

        for cv in cvs:

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(cv.file, tmp)
                tmp_path = tmp.name

            try:

                parsed_cv = extract_cv_data(tmp_path)

                cv_text = build_cv_text(parsed_cv)

                # ✅ التعديل هنا: استخراج cv_id من اسم الملف
                cv_id = cv.filename.replace(".pdf", "")

                parsed_cv["cv_text"] = cv_text
                parsed_cv["cv_id"] = cv_id  # ✅ ربط الـ ID

                parsed_cvs.append(parsed_cv)

            finally:

                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        job_data = parse_job_description(job_description)
        job_text = build_job_text(job_data)

        ranked_results = rank_candidates(
            parsed_cvs=parsed_cvs,
            job_text=job_text,
            job_data=job_data
        )

        # ✅ مفيش تعديل هنا لأن to_dict بقى بيرجع cv_id
        return [result.to_dict() for result in ranked_results]

    except Exception as e:

        logger.exception("Error during ranking candidates")
        raise HTTPException(status_code=400, detail=str(e))
    