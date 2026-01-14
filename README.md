# 🗳️ Vibe Check – Polling API

A simple REST API for creating polls and casting votes.
Built for the Backend Internship Challenge.

## 🚀 Tech Stack
- Python
- FastAPI
- SQLite
- SQLAlchemy

## ▶️ How to Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
Docs: http://127.0.0.1:8000/docs
📌 Endpoints
POST /polls
GET /polls/{id}
POST /polls/{id}/vote
🔐 One Vote per User Logic
A database-level UNIQUE constraint on (user_id, poll_id) ensures each user can vote only once per poll.

---

## ✅ STEP 4: Commit & Push to YOUR repo
```bash
git status
git add .
git commit -m "Implemented Vibe Check Polling API backend"
git push origin main
✅ STEP 5: Final Check (VERY IMPORTANT)
Bash
pip install -r requirements.txt
uvicorn app.main:app --reload
Open
http://127.0.0.1:8000/docs
