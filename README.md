# 🚀 Smart Recruitment AI System

AI-powered recruitment system that analyzes CVs and ranks candidates based on job descriptions.

---

## 📌 Overview
This system helps HR teams automatically evaluate and rank candidates using Artificial Intelligence.

It processes CVs, compares them with job requirements, and returns a ranked list with explanations.

---


## 🔄 Workflow

1. HR uploads CVs
2. Backend assigns cv_id for each CV
3. Backend sends CVs + job description to AI service
4. AI parses CVs
5. AI calculates match score
6. AI ranks candidates


---

## ⚙️ Tech Stack

- Python (FastAPI)
- Sentence Transformers (NLP)
- Docker
- REST API


---

## 🔥 Features

- CV Parsing (Skills, Experience, Title)
- Semantic Matching (AI-based)
- Candidate Ranking System
- Explainable AI (why accepted/rejected)


---


🚀 Run Locally

uvicorn app.main:app --reload

🐳 Run with Docker

docker build -t smart-recruitment-ai
docker run -p 8000:8000 smart-recruitment-ai

📡 API Endpoints
POST /api/ai/parse-cv
POST /api/ai/match-job
POST /api/ai/rank-candidates
