# ATM Cash Intelligence ML

Reusable ML package for hourly ATM withdrawal forecasting and balance depletion
simulation.

The ML layer remains independent from the frontend and backend. It owns:

- training data and notebooks
- feature engineering
- model training
- model/preprocessor artifacts
- recursive withdrawal forecasting
- depletion simulation logic

## Train

```bash
cd ml
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Artifacts are written to:

```text
ml/artifacts/
```

## Main Files

- `src/components/data_ingestion.py`
- `src/components/data_transformation.py`
- `src/components/model_trainer.py`
- `src/components/depletion_simulator.py`
- `src/pipelines/train_pipeline.py`
- `src/pipelines/predict_pipeline.py`

The backend imports this ML package and calls `PredictionPipeline`.
