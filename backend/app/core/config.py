import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ML_ROOT = PROJECT_ROOT / "ml"


@dataclass(frozen=True)
class Settings:
    app_name: str = "ATM Cash Intelligence API"
    api_version: str = "1.0.0"
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    )
    ml_root: Path = ML_ROOT
    model_path: Path = ML_ROOT / "artifacts" / "model.joblib"
    preprocessor_path: Path = ML_ROOT / "artifacts" / "preprocessor.joblib"
    history_data_path: Path = ML_ROOT / "artifacts" / "raw_data.csv"
    default_low_balance_threshold: float = float(
        os.getenv("LOW_BALANCE_THRESHOLD", "5000")
    )
    default_forecast_horizon_hours: int = int(os.getenv("FORECAST_HORIZON_HOURS", "72"))


settings = Settings()
