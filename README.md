🔥 Smart Recruitment AI

AI-powered Applicant Tracking System (ATS) microservice built with FastAPI.

🚀 Overview

Smart Recruitment AI is an intelligent recruitment microservice designed to:

📄 Parse CV PDFs

🧠 Extract structured candidate data

🎯 Match candidates with job descriptions

📊 Calculate match score (0–100%)

✅ Provide hiring decision (ACCEPT / PENDING / REJECT)

🏗️ Architecture

The AI runs as a FastAPI microservice with the following endpoints:

📌 Endpoints
POST /api/ai/parse-cv

Parses and extracts structured data from a CV file.

POST /api/ai/match-job

Matches a parsed CV against a job description and returns:

match_score (percentage)

decision (ACCEPT / PENDING / REJECT)

details

raw_score

semantic_score

extracted skills

predicted title

experience level

🧠 AI Components

Sentence Transformers (semantic similarity)

Skill extraction engine

Missing skills detection

Ranking system

Decision threshold logic

🛠️ Tech Stack

Python

FastAPI

PyTorch

Transformers

scikit-learn

spaCy

PDF parsing tools

📊 Decision Logic
The final hiring decision is based on configurable thresholds:

ACCEPT → High match

PENDING → Medium match

REJECT → Low match

Thresholds can be adjusted in the configuration file.

🎓 Project Context
This project was developed as a Graduation Project focused on applying AI in recruitment automation and decision support systems.



## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs

