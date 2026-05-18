# ATM Cash Demand Predictor

An end-to-end machine learning project for forecasting ATM cash withdrawal demand.

The current pipeline ingests cleaned ATM transaction data, performs a time-aware
train/test split, builds time and lag-based features, trains a regression model,
and writes model artifacts plus evaluation metrics.

## Dataset

The project uses ATM transaction records with fields such as:

- `atmId`
- `totalBalance`
- `totalOutcome`
- `totalNumberTransaction`
- `day`
- `transactionTime`

The default prediction target is `totalOutcome`, which represents withdrawal
cash demand for a transaction period.

## Project Structure

```text
src/
  components/
    data_ingestion.py
    data_transformation.py
    model_trainer.py
  pipelines/
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

## Evaluation

The model currently reports:

- Mean Absolute Error
- Root Mean Squared Error
- R2 score

MAE is especially useful for this project because it maps directly to average
cash amount error.

## Modeling Notes

The split is based on `transactionTime` instead of a random split, which better
matches a real forecasting workflow. The model avoids using same-period outcome
fields as input features and instead uses previous ATM behavior, rolling demand,
and timestamp-derived features.
