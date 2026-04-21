from fastapi import APIRouter, HTTPException

from app.schemas.prediction import (
    PredictRiskRequest,
    PredictRiskResponse,
    TurnoverPredictionRequest,
    TurnoverPredictionResponse,
)
from app.services.prediction import run_predict_risk, run_turnover_prediction

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=TurnoverPredictionResponse)
def predict_turnover(payload: TurnoverPredictionRequest) -> TurnoverPredictionResponse:
    result, err = run_turnover_prediction(payload)
    if err is not None:
        if err.startswith("Prediction failed"):
            raise HTTPException(status_code=400, detail=err)
        raise HTTPException(status_code=503, detail=err)
    return result


@router.post("/predict-risk", response_model=PredictRiskResponse)
def predict_risk(payload: PredictRiskRequest) -> PredictRiskResponse:
    result, err = run_predict_risk(payload)
    if err is not None:
        if err.startswith("Prediction failed"):
            raise HTTPException(status_code=400, detail=err)
        raise HTTPException(status_code=503, detail=err)
    return result
