"""Run inference using the cached joblib model."""

from __future__ import annotations

import math

import pandas as pd

from app.models.employee import Employee
from app.schemas.prediction import (
    PredictRiskRequest,
    PredictRiskResponse,
    TurnoverPredictionRequest,
    TurnoverPredictionResponse,
)
from app.services.ml_model import load_model_once
from app.services.prediction_fallback import heuristic_predict_risk, risk_level_from_probability


def predict_request_from_employee(employee: Employee) -> PredictRiskRequest:
    """Build ML input from a persisted ``Employee`` row (existing risk fields are ignored by the model)."""
    return PredictRiskRequest(
        full_name=employee.full_name,
        age=employee.age,
        department=employee.department,
        job_role=employee.job_role,
        monthly_income=float(employee.monthly_income),
        distance_from_home=float(employee.distance_from_home),
        years_at_company=float(employee.years_at_company),
        job_satisfaction=employee.job_satisfaction,
        environment_satisfaction=employee.environment_satisfaction,
        work_life_balance=employee.work_life_balance,
        training_times_last_year=employee.training_times_last_year,
        attendance_score=float(employee.attendance_score),
        task_completion_rate=float(employee.task_completion_rate),
        onboarding_feedback=employee.onboarding_feedback or "",
        risk_score=float(employee.risk_score),
        risk_level=employee.risk_level,
    )


def _row_to_dataframe(row: dict) -> pd.DataFrame:
    return pd.DataFrame([row])


def predict_with_model(model, feature_row: dict) -> tuple[int, float | None]:
    """Run ``predict`` / ``predict_proba`` on one row (IBM-style column names)."""
    X = _row_to_dataframe(feature_row)
    pred = model.predict(X)
    label = int(pred[0])
    proba: float | None = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        proba = float(probs[1]) if len(probs) > 1 else float(probs[0])
    return label, proba


def employee_to_model_features(employee: PredictRiskRequest) -> dict:
    """
    Map app employee fields to the column names expected by ``model.pkl``.

    Fields without a direct match use simple defaults so the pipeline always
    receives a full feature row.
    """
    yac = int(max(0, round(employee.years_at_company)))
    mi = int(max(0, round(employee.monthly_income)))

    return {
        "Age": int(employee.age),
        "BusinessTravel": "Travel_Rarely",
        "DailyRate": int(max(1, round(mi * 12 / 261))) if mi else 800,
        "Department": str(employee.department).strip(),
        "DistanceFromHome": int(max(0, round(employee.distance_from_home))),
        "Education": 3,
        "EducationField": "Life Sciences",
        "EnvironmentSatisfaction": int(employee.environment_satisfaction),
        "Gender": "Male",
        "HourlyRate": int(max(1, min(100, round(mi / 160)))) if mi else 65,
        "JobInvolvement": 3,
        "JobLevel": 2,
        "JobRole": str(employee.job_role).strip(),
        "JobSatisfaction": int(employee.job_satisfaction),
        "MaritalStatus": "Single",
        "MonthlyIncome": mi,
        "MonthlyRate": int(max(1, round(mi * 2.73))) if mi else 14000,
        "NumCompaniesWorked": max(1, min(9, yac // 3 + 1)),
        "OverTime": "No",
        "PercentSalaryHike": 15,
        "PerformanceRating": 3,
        "RelationshipSatisfaction": 3,
        "StockOptionLevel": 1,
        "TotalWorkingYears": max(yac, yac + 3),
        "TrainingTimesLastYear": int(employee.training_times_last_year),
        "WorkLifeBalance": int(employee.work_life_balance),
        "YearsAtCompany": yac,
        "YearsInCurrentRole": max(0, min(yac, 5)),
        "YearsSinceLastPromotion": max(0, min(yac, 3)),
        "YearsWithCurrManager": max(0, min(yac, 5)),
    }


def run_turnover_prediction(
    payload: TurnoverPredictionRequest,
) -> tuple[TurnoverPredictionResponse | None, str | None]:
    """
    Returns ``(response, None)`` on success, or ``(None, message)`` if the model
    is missing/unreadable or prediction raises.
    """
    model, load_err = load_model_once()
    if load_err is not None:
        return None, load_err

    try:
        label, proba = predict_with_model(model, payload.model_dump())
        return TurnoverPredictionResponse(
            predicted_label=label,
            churn_probability=proba,
        ), None
    except Exception as exc:  # noqa: BLE001
        return None, f"Prediction failed: {exc}"


def run_predict_risk(
    payload: PredictRiskRequest,
) -> tuple[PredictRiskResponse | None, str | None]:
    """Employee-style body -> real model if available, else rule-based fallback."""
    model, load_err = load_model_once()
    if load_err is not None:
        return heuristic_predict_risk(payload), None

    row = employee_to_model_features(payload)
    try:
        label, proba = predict_with_model(model, row)
        probability = proba if proba is not None else float(label)
        if not math.isfinite(probability):
            probability = float(label)
        probability = max(0.0, min(1.0, float(probability)))
        return PredictRiskResponse(
            prediction=label,
            probability=probability,
            risk_level=risk_level_from_probability(probability),
        ), None
    except Exception as exc:  # noqa: BLE001
        return None, f"Prediction failed: {exc}"
