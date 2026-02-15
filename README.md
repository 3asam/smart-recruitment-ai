# Smart Recruitment AI 🔥

An AI-powered ATS (Applicant Tracking System) microservice built with FastAPI.

This system:
- Parses CV PDFs
- Extracts structured data
- Matches candidates with job descriptions
- Calculates intelligent similarity scores
- Returns hiring decisions (ACCEPT / PENDING / REJECT)

---

## 🚀 Tech Stack

- FastAPI
- Sentence-Transformers (MiniLM)
- PyTorch
- Scikit-learn
- PDFPlumber
- Python 3.10

---

## 📌 API Endpoints

### 1️⃣ Parse CV

Uploads a CV (PDF) and returns structured extracted data.

---

### 2️⃣ Match Job (ATS Core)

Uploads:
- CV (PDF)
- Job description (text)

Returns:
- Match Score (0–100)
- Decision
- Detailed breakdown

---

## 🧠 Decision Logic

The final decision is based on:

- Semantic similarity
- Skills matching
- Title alignment
- Experience range check

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
