from typing import Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class PredictionRequest(BaseModel):
    atmId: str = Field(..., examples=["atm350000"])
    current_balance: float = Field(..., ge=0, examples=[40000])
    current_datetime: str = Field(..., examples=["2026-05-28 03:00:00"])
    low_balance_threshold: float | None = Field(default=None, ge=0, examples=[5000])
    forecast_horizon_hours: int | None = Field(default=None, ge=1, le=168, examples=[72])


class ForecastPoint(BaseModel):
    hour: int
    forecast_time: str
    predicted_withdrawal: float
    projected_balance: float


class PredictionResponse(BaseModel):
    atmId: str
    hours_until_low_balance: int | None
    estimated_depletion_time: str | None
    risk_level: RiskLevel
    recommended_refill_within_hours: int | None
    low_balance_threshold: float
    forecast_horizon_hours: int
    forecast: list[ForecastPoint]


class ATMStatus(BaseModel):
    atmId: str
    atmName: str | None = None
    atmCity: str | None = None
    current_balance: float
    risk_level: RiskLevel
    hours_until_low_balance: int | None
    estimated_depletion_time: str | None
    recommended_refill_within_hours: int | None


class ATMListResponse(BaseModel):
    total_atms: int
    critical_atms: int
    high_risk_atms: int
    medium_risk_atms: int
    safe_atms: int
    atms: list[ATMStatus]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    preprocessor_loaded: bool
    history_loaded: bool
