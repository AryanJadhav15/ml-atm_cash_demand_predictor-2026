import sys
from functools import cached_property, lru_cache
from time import time

import pandas as pd

from app.core.config import settings

sys.path.insert(0, str(settings.ml_root))

from src.pipelines.predict_pipeline import PredictionPipeline, PredictionPipelineConfig  # noqa: E402


class ATMIntelligenceService:
    def __init__(self):
        self.pipeline = PredictionPipeline(
            PredictionPipelineConfig(
                model_path=str(settings.model_path),
                preprocessor_path=str(settings.preprocessor_path),
                default_low_balance_threshold=settings.default_low_balance_threshold,
                default_forecast_horizon_hours=settings.default_forecast_horizon_hours,
            )
        )
        self._atm_status_cache = None
        self._atm_status_cache_time = 0
        self._atm_status_cache_ttl_seconds = 300

    @cached_property
    def history_df(self):
        df = pd.read_csv(settings.history_data_path)
        df["transactionTime"] = pd.to_datetime(df["transactionTime"], errors="raise")
        return df.sort_values(["atmId", "transactionTime"]).reset_index(drop=True)

    def health(self):
        return {
            "status": "ok",
            "model_loaded": self.pipeline.model is not None,
            "preprocessor_loaded": self.pipeline.preprocessor is not None,
            "history_loaded": not self.history_df.empty,
        }

    def predict(
        self,
        atm_id,
        current_balance,
        current_datetime,
        low_balance_threshold=None,
        forecast_horizon_hours=None,
    ):
        recent_history = self._recent_history(atm_id)
        return self.pipeline.predict_time_until_low_balance(
            atm_id=atm_id,
            current_balance=current_balance,
            current_datetime=current_datetime,
            recent_history=recent_history,
            low_balance_threshold=low_balance_threshold,
            forecast_horizon_hours=forecast_horizon_hours,
        )

    def get_all_atm_statuses(self):
        if (
            self._atm_status_cache is not None
            and time() - self._atm_status_cache_time < self._atm_status_cache_ttl_seconds
        ):
            return self._atm_status_cache

        statuses = []
        latest_rows = (
            self.history_df.sort_values("transactionTime").groupby("atmId", as_index=False).tail(1)
        )

        for _, row in latest_rows.iterrows():
            result = self._estimate_fleet_status(row)
            statuses.append(
                {
                    "atmId": row["atmId"],
                    "atmName": row.get("atmName"),
                    "atmCity": row.get("atmCity"),
                    "current_balance": float(row["totalBalance"]),
                    "risk_level": result["risk_level"],
                    "hours_until_low_balance": result["hours_until_low_balance"],
                    "estimated_depletion_time": result["estimated_depletion_time"],
                    "recommended_refill_within_hours": result[
                        "recommended_refill_within_hours"
                    ],
                }
            )

        statuses = sorted(
            statuses,
            key=lambda item: (
                self._risk_rank(item["risk_level"]),
                item["hours_until_low_balance"] if item["hours_until_low_balance"] is not None else 999,
            ),
        )
        response = {
            "total_atms": len(statuses),
            "critical_atms": self._count_risk(statuses, "CRITICAL"),
            "high_risk_atms": self._count_risk(statuses, "HIGH"),
            "medium_risk_atms": self._count_risk(statuses, "MEDIUM"),
            "safe_atms": self._count_risk(statuses, "LOW"),
            "atms": statuses,
        }
        self._atm_status_cache = response
        self._atm_status_cache_time = time()
        return response

    def get_forecast(self, atm_id):
        latest_row = self._latest_row(atm_id)
        result = self.predict(
            atm_id=atm_id,
            current_balance=float(latest_row["totalBalance"]),
            current_datetime=latest_row["transactionTime"],
            forecast_horizon_hours=72,
        )
        return result

    def get_filters(self):
        cities = sorted(self.history_df["atmCity"].dropna().unique().tolist())
        raw_names = self.history_df["atmName"].dropna().unique()
        banks = sorted(list(set(name.split(" ATM -")[0] for name in raw_names if " ATM -" in name)))
        return {
            "cities": cities,
            "banks": banks
        }


    def _recent_history(self, atm_id, rows=48):
        atm_history = self.history_df[self.history_df["atmId"] == atm_id].tail(rows)
        if atm_history.empty:
            raise ValueError(f"Unknown ATM ID: {atm_id}")
        return atm_history

    def _latest_row(self, atm_id):
        return self._recent_history(atm_id, rows=1).iloc[-1]

    def _count_risk(self, statuses, risk_level):
        return sum(1 for status in statuses if status["risk_level"] == risk_level)

    def _risk_rank(self, risk_level):
        return {
            "CRITICAL": 0,
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3,
        }.get(risk_level, 4)

    def _estimate_fleet_status(self, latest_row):
        atm_id = latest_row["atmId"]
        current_balance = float(latest_row["totalBalance"])
        threshold = settings.default_low_balance_threshold
        recent_history = self._recent_history(atm_id, rows=12)
        recent_withdrawals = recent_history["totalOutcome"].astype(float).tail(6)
        hourly_withdrawal_rate = max(float(recent_withdrawals.mean()), 1.0)

        if current_balance <= threshold:
            hours_until_low_balance = 0
        else:
            hours_until_low_balance = int(
                (current_balance - threshold) // hourly_withdrawal_rate
            )

        depletion_time = pd.to_datetime(latest_row["transactionTime"]) + pd.Timedelta(
            hours=hours_until_low_balance
        )
        risk_level = self._risk_level(hours_until_low_balance)

        return {
            "risk_level": risk_level,
            "hours_until_low_balance": hours_until_low_balance,
            "estimated_depletion_time": depletion_time.strftime("%Y-%m-%d %H:%M:%S"),
            "recommended_refill_within_hours": self._recommended_refill_window(
                hours_until_low_balance,
                risk_level,
            ),
        }

    def _risk_level(self, hours_until_low_balance):
        if hours_until_low_balance <= 6:
            return "CRITICAL"
        if hours_until_low_balance <= 12:
            return "HIGH"
        if hours_until_low_balance <= 24:
            return "MEDIUM"
        return "LOW"

    def _recommended_refill_window(self, hours_until_low_balance, risk_level):
        buffer_hours = {
            "CRITICAL": 1,
            "HIGH": 3,
            "MEDIUM": 6,
            "LOW": 12,
        }[risk_level]
        return max(0, hours_until_low_balance - buffer_hours)


@lru_cache(maxsize=1)
def get_atm_service():
    return ATMIntelligenceService()
