from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import tempfile
import shutil
import os
import logging
import uuid

from app.parsing.cv_parser.parser import extract_cv_data
from app.parsing.adapter import build_cv_text
from app.parsing.job_adapter import build_job_text
from app.parsing.job_parser import parse_job_description

from app.matching.final_score import calculate_final_score
from app.matching.ranking import rank_candidates
from app.core.model_loader import load_model


# ==========================================
# Logging
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==========================================
# App Init
# ==========================================
app = FastAPI(
    title="Smart Recruitment AI Service",
    version="10.0"
)


# ==========================================
# Startup
# ==========================================
@app.on_event("startup")
def startup_event():
    logger.info("Starting Smart Recruitment AI service...")
    load_model()
    logger.info("AI model loaded.")


# ==========================================
# Health Check
# ==========================================
@app.get("/health")
def health():
    return {"status": "ok"}


# ==========================================
# Parse CV
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

        return {
            "data": parsed_cv
        }

    except Exception as e:
        logger.exception("Error parsing CV")
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# Match Single CV
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

        # 🔥 Generate CV ID
        cv_id = f"CV-{str(uuid.uuid4())[:8].upper()}"

        result = calculate_final_score(
            cv_text=cv_text,
            job_text=job_text,
            job_data=job_data,
            parsed_cv=parsed_cv,
            cv_id=cv_id
        )

        return result.to_dict()

    except Exception as e:
        logger.exception("Error matching job")
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

                # 🔥 Generate cv_id لكل CV
                cv_id = f"CV-{str(uuid.uuid4())[:8].upper()}"

                parsed_cv["cv_text"] = cv_text
                parsed_cv["cv_id"] = cv_id   # 🔥 الحل الأساسي

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

        return [result.to_dict() for result in ranked_results]

    except Exception as e:
        logger.exception("Error ranking candidates")
        raise HTTPException(status_code=400, detail=str(e))


# ==========================================
# Simple Ranking (Light Response)
# ==========================================
@app.post("/api/ai/rank-simple")
async def rank_simple_endpoint(
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

                cv_id = f"CV-{str(uuid.uuid4())[:8].upper()}"

                parsed_cv["cv_text"] = cv_text
                parsed_cv["cv_id"] = cv_id

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

        return [
            {
                "rank": i + 1,
                "cv_id": r.cv_id,
                "match_score": r.match_score,
                "decision": r.decision
            }
            for i, r in enumerate(ranked_results)
        ]

    except Exception as e:
        logger.exception("Error in simple ranking")
        raise HTTPException(status_code=400, detail=str(e))
    
    