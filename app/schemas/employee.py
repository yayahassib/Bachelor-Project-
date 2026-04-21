from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    """Fields sent when creating an employee (same as the table, without `id`)."""

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


class EmployeeResponse(BaseModel):
    """Employee as returned by the API (includes database `id`)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
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
    onboarding_feedback: str
    risk_score: float
    risk_level: str
