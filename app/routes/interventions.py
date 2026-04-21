from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.models.intervention import Intervention
from app.schemas import InterventionCreate, InterventionResponse

router = APIRouter(tags=["interventions"])


@router.post(
    "/interventions",
    response_model=InterventionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_intervention(
    payload: InterventionCreate,
    db: Session = Depends(get_db),
) -> InterventionResponse:
    if db.get(Employee, payload.employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    intervention = Intervention(**payload.model_dump())
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    return intervention


@router.get(
    "/interventions/{employee_id}",
    response_model=list[InterventionResponse],
)
def list_interventions_for_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> list[InterventionResponse]:
    if db.get(Employee, employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    stmt = (
        select(Intervention)
        .where(Intervention.employee_id == employee_id)
        .order_by(Intervention.date_applied.desc(), Intervention.id.desc())
    )
    return list(db.scalars(stmt).all())
