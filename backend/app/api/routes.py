from fastapi import APIRouter, HTTPException

from app.schemas.prediction import (
    ATMFiltersResponse,
    ATMListResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
)
from app.services.ml_service import get_atm_service


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return get_atm_service().health()


@router.post("/predict", response_model=PredictionResponse)
def predict_atm_depletion(payload: PredictionRequest):
    try:
        return get_atm_service().predict(
            atm_id=payload.atmId,
            current_balance=payload.current_balance,
            current_datetime=payload.current_datetime,
            low_balance_threshold=payload.low_balance_threshold,
            forecast_horizon_hours=payload.forecast_horizon_hours,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/atms", response_model=ATMListResponse)
def get_atm_statuses():
    return get_atm_service().get_all_atm_statuses()


@router.get("/atms/filters", response_model=ATMFiltersResponse)
def get_atm_filters():
    return get_atm_service().get_filters()


@router.get("/atm/{atm_id}/forecast", response_model=PredictionResponse)
def get_atm_forecast(atm_id: str):
    try:
        return get_atm_service().get_forecast(atm_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
