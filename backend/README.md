# Backend Run Guide

## Local Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.api.main:app --reload
```

## Docker

```bash
docker compose up --build
```

Backend:
- http://localhost:8000
- /health endpoint available
