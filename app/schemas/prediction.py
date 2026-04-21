"""Request/response shapes for the turnover model (same feature names as training data)."""

from pydantic import BaseModel, ConfigDict


class TurnoverPredictionRequest(BaseModel):
    """One row of features matching the IBM HR-style columns used to train ``model.pkl``."""

    model_config = ConfigDict(extra="forbid")

    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int


class TurnoverPredictionResponse(BaseModel):
    predicted_label: int
    churn_probability: float | None = None


class PredictRiskRequest(BaseModel):
    """Same shape as employee create payload; ``risk_score`` / ``risk_level`` are ignored for ML input."""

    full_name: str
    age: int
    department: str
    job_role: str
    monthly_income: float
    distance_from_home: float
    years_at_company: float
    job_satisfaction: int
    environment_satisfaction: int
    work_life_balance: int
    training_times_last_year: int
    attendance_score: float
    task_completion_rate: float
    onboarding_feedback: str = ""
    risk_score: float
    risk_level: str


class PredictRiskResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str
