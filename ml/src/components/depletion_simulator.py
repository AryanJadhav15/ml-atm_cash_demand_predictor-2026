from dataclasses import dataclass

import pandas as pd


@dataclass
class DepletionSimulationConfig:
    low_balance_threshold: float = 5000
    forecast_horizon_hours: int = 72
    refill_buffer_hours: int = 3


class DepletionSimulator:
    def __init__(self, config=None):
        self.config = config or DepletionSimulationConfig()

    def simulate(self, current_balance, current_datetime, hourly_predictions):
        current_datetime = pd.to_datetime(current_datetime)
        balance = float(current_balance)
        forecast_rows = []
        low_balance_time = None

        for hour_number, predicted_withdrawal in enumerate(hourly_predictions, start=1):
            predicted_withdrawal = max(0.0, float(predicted_withdrawal))
            balance_after_withdrawal = balance - predicted_withdrawal
            forecast_time = current_datetime + pd.Timedelta(hours=hour_number)

            forecast_rows.append(
                {
                    "hour": hour_number,
                    "forecast_time": forecast_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "predicted_withdrawal": round(predicted_withdrawal, 2),
                    "projected_balance": round(balance_after_withdrawal, 2),
                }
            )

            balance = balance_after_withdrawal
            if balance <= self.config.low_balance_threshold:
                low_balance_time = forecast_time
                break

        if low_balance_time is None:
            hours_until_low_balance = None
            risk_level = "LOW"
            recommended_refill_within_hours = None
        else:
            hours_until_low_balance = len(forecast_rows)
            risk_level = self._risk_level(hours_until_low_balance)
            recommended_refill_within_hours = max(
                0,
                hours_until_low_balance - self._refill_buffer_for_risk(risk_level),
            )

        return {
            "hours_until_low_balance": hours_until_low_balance,
            "estimated_depletion_time": (
                low_balance_time.strftime("%Y-%m-%d %H:%M:%S")
                if low_balance_time is not None
                else None
            ),
            "risk_level": risk_level,
            "recommended_refill_within_hours": recommended_refill_within_hours,
            "low_balance_threshold": self.config.low_balance_threshold,
            "forecast_horizon_hours": self.config.forecast_horizon_hours,
            "forecast": forecast_rows,
        }

    def _risk_level(self, hours_until_low_balance):
        if hours_until_low_balance <= 6:
            return "CRITICAL"
        if hours_until_low_balance <= 12:
            return "HIGH"
        if hours_until_low_balance <= 24:
            return "MEDIUM"
        return "LOW"

    def _refill_buffer_for_risk(self, risk_level):
        return {
            "CRITICAL": 1,
            "HIGH": self.config.refill_buffer_hours,
            "MEDIUM": 6,
            "LOW": 12,
        }.get(risk_level, self.config.refill_buffer_hours)
