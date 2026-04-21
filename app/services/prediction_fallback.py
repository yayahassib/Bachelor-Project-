"""
Rule-based risk when ``model.pkl`` is missing.

For local / frontend testing only. Real scoring lives in ``prediction.py`` + joblib.
"""

from app.schemas.prediction import PredictRiskRequest, PredictRiskResponse


def risk_level_from_probability(probability: float) -> str:
    """Same bands as production: Low below 0.40, Medium below 0.70, else High."""
    if probability < 0.40:
        return "Low"
    if probability < 0.70:
        return "Medium"
    return "High"


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _norm_scale(value: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.5
    c = max(lo, min(hi, value))
    return (c - lo) / (hi - lo)


def heuristic_predict_risk(payload: PredictRiskRequest) -> PredictRiskResponse:
    """
    Estimate churn probability from a few fields (not the ML model).

    Better satisfaction, work–life balance, attendance, and task completion
    → lower probability (better retention).
    """
    sat = _norm_scale(float(payload.job_satisfaction), 1.0, 5.0)
    wlb = _norm_scale(float(payload.work_life_balance), 1.0, 5.0)
    att = _norm_scale(float(payload.attendance_score), 0.0, 100.0)
    t = float(payload.task_completion_rate)
    task = t / 100.0 if t > 1.0 else t
    task = _clamp01(task)

    wellbeing = (sat + wlb + att + task) / 4.0
    probability = _clamp01(1.0 - wellbeing)
    prediction = 1 if probability >= 0.5 else 0

    return PredictRiskResponse(
        prediction=prediction,
        probability=probability,
        risk_level=risk_level_from_probability(probability),
    )
