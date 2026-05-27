# ATM Cash Depletion Predictor

An end-to-end machine learning project for estimating how much time remains before
an ATM reaches a low cash balance.

The model still predicts hourly withdrawal demand internally, but the business
output is now depletion risk:

- estimated hours until low balance
- estimated low-balance/depletion time
- refill recommendation
- risk level

## Dataset

The project uses ATM transaction records with fields such as:

- `atmId`
- `totalBalance`
- `totalOutcome`
- `totalNumberTransaction`
- `day`
- `transactionTime`

The internal model target is `totalOutcome`, which represents withdrawal cash
demand for a transaction period. The final decision target is the number of
hours until the ATM reaches a configured low-balance threshold.

## Project Structure

```text
src/
  components/
    data_ingestion.py
    data_transformation.py
    depletion_simulator.py
    model_trainer.py
  pipelines/
    predict_pipeline.py
    train_pipeline.py
  notebooks/
    data/
artifacts/
  raw_data.csv
  train_data.csv
  test_data.csv
```

## Setup

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

## Run Training

```bash
python app.py
```

The pipeline writes:

- `artifacts/raw_data.csv`
- `artifacts/train_data.csv`
- `artifacts/test_data.csv`
- `artifacts/preprocessor.joblib`
- `artifacts/model.joblib`
- `artifacts/metrics.json`

## Run Inference

```python
import pandas as pd
from src.pipelines.predict_pipeline import PredictionPipeline

history = pd.read_csv("artifacts/raw_data.csv")
atm_id = "atm350000"
recent_history = history[history["atmId"] == atm_id].tail(24)

result = PredictionPipeline().predict_time_until_low_balance(
    atm_id=atm_id,
    current_balance=40000,
    current_datetime="2026-05-28 03:00:00",
    recent_history=recent_history,
    low_balance_threshold=5000,
    forecast_horizon_hours=72,
)
print(result)
```

## Evaluation

The internal hourly withdrawal model reports:

- Mean Absolute Error
- Root Mean Squared Error
- R2 score

MAE is especially useful for this project because it maps directly to average
cash amount error. The production business metric should also track whether the
system predicted the low-balance time early enough for a successful refill.

## Modeling Notes

The split is based on `transactionTime` instead of a random split, which better
matches a real forecasting workflow. The model avoids using same-period outcome
fields as input features and instead uses previous ATM behavior, rolling demand,
and timestamp-derived features.

The depletion pipeline recursively forecasts future hourly withdrawals, subtracts
each predicted withdrawal from the current balance, and stops when projected
balance reaches the low-balance threshold.
