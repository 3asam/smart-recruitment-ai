Smart Recruitment AI

AI-powered Applicant Tracking System (ATS) microservice built with FastAPI.

Overview

Smart Recruitment AI is an intelligent recruitment microservice designed to automate:

CV parsing and structured data extraction

Candidate–job semantic matching

Match scoring (0–100%)

Hiring decision support (ACCEPT / PENDING / REJECT)

Candidate ranking based on job fit

The system is built as a modular, production-ready FastAPI service.

Architecture

The system follows a layered architecture:

API Layer (FastAPI endpoints)

AI & Matching Engine

Scoring & Decision Logic

Parsing & Skill Extraction Modules

Project structure:

smart-recruitment-ai/
│
├── main.py              # Entry point
├── app/
│   ├── main.py          # FastAPI app
│   ├── parsing/         # CV parsing logic
│   ├── matching/        # Matching & ranking engine
│   ├── core/            # Embeddings & model loading
│   ├── schemas/         # Request/response models
│   └── config/          # Thresholds & settings
│
└── requirements.txt

API Endpoints
POST /api/ai/parse-cv

Extracts structured information from a CV.

POST /api/ai/match-job

Matches a candidate against a job description and returns:

match_score (percentage)

decision (ACCEPT / PENDING / REJECT)

raw_score

semantic_score

missing_skills

extracted skills

experience evaluation

POST /api/ai/rank-candidates

Ranks multiple candidates against a job description based on match score.

AI Components

Semantic similarity using Sentence Transformers

Skill extraction and normalization

Experience alignment logic

Missing skills detection

Configurable decision thresholds

Technology Stack

Python

FastAPI

PyTorch

Transformers

scikit-learn

spaCy

PDF parsing tools

🏗️ System Design
High-Level Architecture
                ┌──────────────────────┐
                │   Frontend / ATS     │
                └──────────┬───────────┘
                           │ HTTP Request
                           ▼
                ┌──────────────────────┐
                │   FastAPI Layer      │
                │  (API Endpoints)     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Parsing Engine      │
                │  (CV Extraction)     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Matching Engine     │
                │  - Semantic Similarity
                │  - Skill Scoring
                │  - Experience Check
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Scoring & Decision  │
                │  Threshold Logic     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   JSON Response      │
                │  Score + Decision    │
                └──────────────────────┘

🔄 Request Flow

Client sends CV and Job Description.

CV is parsed into structured data.

Embeddings are generated for semantic comparison.

Skill and experience alignment is calculated.

A weighted scoring algorithm computes the final score.

Decision thresholds determine ACCEPT / PENDING / REJECT.

Structured response is returned.

🧠 AI Processing Pipeline
Raw CV
   ↓
Text Extraction
   ↓
Skill Extraction
   ↓
Embedding Generation (Sentence Transformers)
   ↓
Semantic Similarity Calculation
   ↓
Skill Overlap Scoring
   ↓
Experience Validation
   ↓
Weighted Final Score
   ↓
Decision Logic

🎯 Design Principles

Separation of Concerns (API vs AI logic)

Modular architecture for scalability

Extensible scoring pipeline

Microservice-ready deployment

Configurable decision thresholds

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs


