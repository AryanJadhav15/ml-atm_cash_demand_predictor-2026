# ATM Cash Intelligence System

Production-style full-stack ATM monitoring platform.

## Architecture

```text
project-root/
  ml/        reusable forecasting and depletion simulation package
  backend/   FastAPI REST service that loads ML artifacts
  frontend/  React/Vite operations dashboard
```

The frontend never reads ML files directly. It communicates only with the
FastAPI backend. The backend loads `ml/artifacts/model.joblib`,
`ml/artifacts/preprocessor.joblib`, and ATM history data, then returns depletion
predictions through REST APIs.

## Run Locally

### 1. ML

```bash
cd ml
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## APIs

- `GET /health`
- `POST /predict`
- `GET /atms`
- `GET /atm/{atm_id}/forecast`

## Business Goal

The system estimates how long each ATM can continue serving customers before
cash falls below the configured low-balance threshold. It supports refill
planning, risk prioritization, and cash-out prevention.
