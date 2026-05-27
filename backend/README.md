# ATM Cash Intelligence Backend

FastAPI service that exposes ATM depletion intelligence to the frontend.

## Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

If you want to use the Uvicorn CLI directly, run it without reload:

```bash
python -m uvicorn app.main:app --app-dir . --port 8000
```

In this project path, Uvicorn's reload subprocess can fail to resolve
`app.main` even when a direct Python import succeeds. The non-reload command and
`run.py` avoid that issue.

## APIs

- `GET /health`
- `POST /predict`
- `GET /atms`
- `GET /atm/{atm_id}/forecast`

The backend loads ML artifacts from `../ml/artifacts` and reads ATM history from
`../ml/artifacts/raw_data.csv`.
