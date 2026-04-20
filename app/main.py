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
    version="7.0"
)


# ==========================================
# Startup Event
# ==========================================
@app.on_event("startup")
def startup_event():
    logger.info("Starting Smart Recruitment AI service...")
    load_model()
    logger.info("AI model loaded at startup.")


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
    cv: UploadFile = File(...),
    cv_id: str = Form(...)
):
    try:

        if not cv_id:
            raise HTTPException(status_code=400, detail="cv_id is required")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(cv.file, tmp)
            tmp_path = tmp.name

        parsed_cv = extract_cv_data(tmp_path)

        return {
            "cv_id": cv_id,
            "data": parsed_cv
        }

    except Exception as e:
        logger.exception("Error while parsing CV")
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# Match Job (Single)
# ==========================================
@app.post("/api/ai/match-job")
async def match_job_endpoint(
    cv: UploadFile = File(...),
    cv_id: str = Form(...),
    job_description: str = Form(...)
):
    try:

        if not cv_id:
            raise HTTPException(status_code=400, detail="cv_id is required")

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
            parsed_cv=parsed_cv,
            cv_id=cv_id
        )

        return result.to_dict()

    except Exception as e:
        logger.exception("Error during job matching")
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ==========================================
# Rank Candidates (FIXED FOR SWAGGER 🔥)
# ==========================================
@app.post("/api/ai/rank-candidates")
async def rank_candidates_endpoint(
    cvs: List[UploadFile] = File(...),
    cv_ids: str = Form(...),  # ✅ string بدل list
    job_description: str = Form(...)
):
    parsed_cvs = []

    try:

        # ✅ نحول string → list
        cv_ids_list = [id.strip() for id in cv_ids.split(",")]

        # ✅ validation
        if len(cvs) != len(cv_ids_list):
            raise HTTPException(
                status_code=400,
                detail="Mismatch between number of cvs and cv_ids"
            )

        for cv, cv_id in zip(cvs, cv_ids_list):

            if not cv_id:
                raise HTTPException(status_code=400, detail="cv_id is required")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(cv.file, tmp)
                tmp_path = tmp.name

            try:
                parsed_cv = extract_cv_data(tmp_path)
                cv_text = build_cv_text(parsed_cv)

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

        # ✅ add rank
        response = []

        for index, result in enumerate(ranked_results, start=1):
            data = result.to_dict()
            data["rank"] = index
            response.append(data)

        return response

    except Exception as e:
        logger.exception("Error during ranking candidates")
        raise HTTPException(status_code=400, detail=str(e))


# ==========================================
# Simple Ranking
# ==========================================
@app.post("/api/ai/rank-simple")
async def rank_simple_endpoint(
    cvs: List[UploadFile] = File(...),
    cv_ids: str = Form(...),
    job_description: str = Form(...)
):
    parsed_cvs = []

    try:

        cv_ids_list = [id.strip() for id in cv_ids.split(",")]

        if len(cvs) != len(cv_ids_list):
            raise HTTPException(
                status_code=400,
                detail="Mismatch between number of cvs and cv_ids"
            )

        for cv, cv_id in zip(cvs, cv_ids_list):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(cv.file, tmp)
                tmp_path = tmp.name

            try:
                parsed_cv = extract_cv_data(tmp_path)
                cv_text = build_cv_text(parsed_cv)

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
    