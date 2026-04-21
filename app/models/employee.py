from __future__ import annotations

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(200))
    age: Mapped[int] = mapped_column(Integer)
    department: Mapped[str] = mapped_column(String(100))
    job_role: Mapped[str] = mapped_column(String(100))
    monthly_income: Mapped[float] = mapped_column(Float)
    distance_from_home: Mapped[float] = mapped_column(Float)
    years_at_company: Mapped[float] = mapped_column(Float)
    job_satisfaction: Mapped[int] = mapped_column(Integer)
    environment_satisfaction: Mapped[int] = mapped_column(Integer)
    work_life_balance: Mapped[int] = mapped_column(Integer)
    training_times_last_year: Mapped[int] = mapped_column(Integer)
    attendance_score: Mapped[float] = mapped_column(Float)
    task_completion_rate: Mapped[float] = mapped_column(Float)
    onboarding_feedback: Mapped[str] = mapped_column(Text, default="")
    risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(50))

    interventions: Mapped[list["Intervention"]] = relationship(
        "Intervention",
        back_populates="employee",
    )
