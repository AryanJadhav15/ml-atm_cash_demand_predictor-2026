import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.components.depletion_simulator import (
    DepletionSimulationConfig,
    DepletionSimulator,
)
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


REQUIRED_HISTORY_COLUMNS = [
    "atmId",
    "atmCity",
    "totalBalance",
    "totalOutcome",
    "totalNumberTransaction",
    "transactionTime",
]


@dataclass
class PredictionPipelineConfig:
    model_path: str = os.path.join("artifacts", "model.joblib")
    preprocessor_path: str = os.path.join("artifacts", "preprocessor.joblib")
    default_low_balance_threshold: float = 5000
    default_forecast_horizon_hours: int = 72


class PredictionPipeline:
    def __init__(self, config=None):
        self.config = config or PredictionPipelineConfig()
        self.model = load_object(self.config.model_path)
        self.preprocessor = load_object(self.config.preprocessor_path)

    def predict_time_until_low_balance(
        self,
        atm_id,
        current_balance,
        current_datetime,
        recent_history,
        low_balance_threshold=None,
        forecast_horizon_hours=None,
    ):
        try:
            low_balance_threshold = (
                low_balance_threshold
                if low_balance_threshold is not None
                else self.config.default_low_balance_threshold
            )
            forecast_horizon_hours = (
                forecast_horizon_hours
                if forecast_horizon_hours is not None
                else self.config.default_forecast_horizon_hours
            )

            history_df = self._prepare_history(recent_history, atm_id)
            hourly_predictions = self._recursive_hourly_forecast(
                atm_id=atm_id,
                current_balance=current_balance,
                current_datetime=current_datetime,
                history_df=history_df,
                forecast_horizon_hours=forecast_horizon_hours,
            )

            simulator = DepletionSimulator(
                DepletionSimulationConfig(
                    low_balance_threshold=low_balance_threshold,
                    forecast_horizon_hours=forecast_horizon_hours,
                )
            )
            result = simulator.simulate(
                current_balance=current_balance,
                current_datetime=current_datetime,
                hourly_predictions=hourly_predictions,
            )
            result["atmId"] = atm_id
            return result
        except Exception as e:
            logging.info("Error Occured in prediction pipeline")
            raise CustomException(e, sys)

    def _recursive_hourly_forecast(
        self,
        atm_id,
        current_balance,
        current_datetime,
        history_df,
        forecast_horizon_hours,
    ):
        simulated_history = history_df.copy()
        simulated_balance = float(current_balance)
        current_datetime = pd.to_datetime(current_datetime)
        predictions = []

        for step in range(1, forecast_horizon_hours + 1):
            future_time = current_datetime + pd.Timedelta(hours=step)
            feature_row = self._build_future_feature_row(
                atm_id=atm_id,
                current_balance=simulated_balance,
                future_time=future_time,
                history_df=simulated_history,
            )
            transformed_features = self.preprocessor.transform(feature_row)
            predicted_withdrawal = max(0.0, float(self.model.predict(transformed_features)[0]))
            predictions.append(predicted_withdrawal)

            simulated_balance -= predicted_withdrawal
            simulated_history = pd.concat(
                [
                    simulated_history,
                    pd.DataFrame(
                        [
                            {
                                "atmId": atm_id,
                                "atmCity": feature_row.iloc[0]["atmCity"],
                                "totalBalance": simulated_balance,
                                "totalOutcome": predicted_withdrawal,
                                "totalNumberTransaction": self._estimated_transaction_count(
                                    simulated_history
                                ),
                                "transactionTime": future_time,
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )

        return predictions

    def _build_future_feature_row(self, atm_id, current_balance, future_time, history_df):
        history_df = history_df.sort_values("transactionTime").reset_index(drop=True)
        atm_city = self._latest_value(history_df, "atmCity", default="unknown")
        outcomes = history_df["totalOutcome"].astype(float)
        balances = history_df["totalBalance"].astype(float)
        transactions = history_df["totalNumberTransaction"].astype(float)

        hour = future_time.hour
        day_of_week = future_time.dayofweek
        outcome_lag_1 = self._lag_value(outcomes, 1, default=0)
        outcome_lag_2 = self._lag_value(outcomes, 2, default=0)
        outcome_lag_3 = self._lag_value(outcomes, 3, default=0)

        return pd.DataFrame(
            [
                {
                    "atmId": atm_id,
                    "atmCity": atm_city,
                    "totalBalance": float(current_balance),
                    "hour": hour,
                    "day_of_week": day_of_week,
                    "month": future_time.month,
                    "is_weekend": int(day_of_week in [5, 6]),
                    "hour_sin": np.sin(2 * np.pi * hour / 24),
                    "hour_cos": np.cos(2 * np.pi * hour / 24),
                    "outcome_lag_1": outcome_lag_1,
                    "outcome_lag_2": outcome_lag_2,
                    "outcome_lag_3": outcome_lag_3,
                    "outcome_lag_6": self._lag_value(outcomes, 6, default=0),
                    "balance_lag_1": self._lag_value(
                        balances,
                        1,
                        default=float(current_balance),
                    ),
                    "transactions_lag_1": self._lag_value(transactions, 1, default=0),
                    "rolling_outcome_mean_3": self._rolling_mean(outcomes, 3),
                    "rolling_outcome_mean_6": self._rolling_mean(outcomes, 6),
                    "rolling_outcome_mean_12": self._rolling_mean(outcomes, 12),
                    "rolling_outcome_std_6": self._rolling_std(outcomes, 6),
                    "outcome_trend_3": outcome_lag_1 - outcome_lag_3,
                    "balance_trend_3": self._lag_value(balances, 1, 0)
                    - self._lag_value(balances, 3, 0),
                }
            ]
        )

    def _prepare_history(self, recent_history, atm_id):
        if isinstance(recent_history, str):
            history_df = pd.read_csv(recent_history)
        else:
            history_df = recent_history.copy()

        missing_columns = [
            column for column in REQUIRED_HISTORY_COLUMNS if column not in history_df.columns
        ]
        if missing_columns:
            raise ValueError(f"Recent history is missing columns: {missing_columns}")

        history_df = history_df[history_df["atmId"] == atm_id].copy()
        if history_df.empty:
            raise ValueError(f"No recent history found for ATM ID: {atm_id}")

        history_df["transactionTime"] = pd.to_datetime(
            history_df["transactionTime"],
            errors="raise",
        )
        history_df = history_df.sort_values("transactionTime").reset_index(drop=True)
        return history_df[REQUIRED_HISTORY_COLUMNS]

    def _lag_value(self, series, periods, default):
        if len(series) < periods:
            return float(default)
        return float(series.iloc[-periods])

    def _rolling_mean(self, series, window):
        if series.empty:
            return 0.0
        return float(series.tail(window).mean())

    def _rolling_std(self, series, window):
        values = series.tail(window)
        if len(values) < 2:
            return 0.0
        return float(values.std())

    def _latest_value(self, df, column, default):
        if df.empty or column not in df.columns:
            return default
        return df.iloc[-1][column]

    def _estimated_transaction_count(self, history_df):
        if history_df.empty:
            return 0
        recent_counts = history_df["totalNumberTransaction"].astype(float).tail(6)
        return int(round(recent_counts.mean()))
