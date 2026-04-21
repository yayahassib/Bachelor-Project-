"""
Insert three sample employees (low / medium / high risk) for UI and API testing.

Run from the project root (folder that contains main.py):

    python seed_sample_employees.py

Or with the venv:

    .\\venv\\Scripts\\python seed_sample_employees.py

Re-running removes any previous rows with the same demo names, then inserts fresh copies.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import delete

from app.database import SessionLocal
from app.models.employee import Employee

DEMO_NAMES = (
    "Demo - Low risk",
    "Demo - Medium risk",
    "Demo - High risk",
)

SAMPLES: list[dict] = [
    {
        "full_name": DEMO_NAMES[0],
        "age": 38,
        "department": "Research & Development",
        "job_role": "Research Scientist",
        "monthly_income": 7200.0,
        "distance_from_home": 6.0,
        "years_at_company": 7.0,
        "job_satisfaction": 5,
        "environment_satisfaction": 5,
        "work_life_balance": 5,
        "training_times_last_year": 3,
        "attendance_score": 97.0,
        "task_completion_rate": 0.94,
        "onboarding_feedback": "Strong onboarding experience.",
        "risk_score": 0.18,
        "risk_level": "Low",
    },
    {
        "full_name": DEMO_NAMES[1],
        "age": 34,
        "department": "Sales",
        "job_role": "Sales Representative",
        "monthly_income": 4800.0,
        "distance_from_home": 22.0,
        "years_at_company": 3.0,
        "job_satisfaction": 3,
        "environment_satisfaction": 3,
        "work_life_balance": 3,
        "training_times_last_year": 1,
        "attendance_score": 82.0,
        "task_completion_rate": 0.72,
        "onboarding_feedback": "Average; role clarity could improve.",
        "risk_score": 0.52,
        "risk_level": "Medium",
    },
    {
        "full_name": DEMO_NAMES[2],
        "age": 29,
        "department": "Human Resources",
        "job_role": "HR Specialist",
        "monthly_income": 3900.0,
        "distance_from_home": 35.0,
        "years_at_company": 1.5,
        "job_satisfaction": 2,
        "environment_satisfaction": 2,
        "work_life_balance": 2,
        "training_times_last_year": 0,
        "attendance_score": 68.0,
        "task_completion_rate": 0.58,
        "onboarding_feedback": "Reported workload and unclear expectations.",
        "risk_score": 0.84,
        "risk_level": "High",
    },
]


def main() -> None:
    with SessionLocal() as db:
        db.execute(delete(Employee).where(Employee.full_name.in_(DEMO_NAMES)))
        db.commit()

        for row in SAMPLES:
            db.add(Employee(**row))
        db.commit()

    print("Inserted 3 sample employees:")
    for name in DEMO_NAMES:
        print(f"  - {name}")
    print("Open /dashboard to see them in the table.")


if __name__ == "__main__":
    main()
