from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.schemas import EmployeeCreate, EmployeeResponse
from app.services.prediction import predict_request_from_employee, run_predict_risk

router = APIRouter(tags=["employees"])


@router.get("/employees", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    risk_level: str | None = Query(default=None),
    department: str | None = Query(default=None),
    sort_by_risk_score: bool = Query(
        default=False,
        description="If true, order by highest risk_score first",
    ),
) -> list[EmployeeResponse]:
    stmt = select(Employee)

    if risk_level is not None:
        stmt = stmt.where(Employee.risk_level == risk_level)
    if department is not None:
        stmt = stmt.where(Employee.department == department)

    if sort_by_risk_score:
        stmt = stmt.order_by(desc(Employee.risk_score), Employee.id)
    else:
        stmt = stmt.order_by(Employee.id)

    return list(db.scalars(stmt).all())


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)) -> EmployeeResponse:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post(
    "/employees/{employee_id}/predict-risk",
    response_model=EmployeeResponse,
)
def predict_risk_for_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    result, err = run_predict_risk(predict_request_from_employee(employee))
    if err is not None:
        if err.startswith("Prediction failed"):
            raise HTTPException(status_code=400, detail=err)
        raise HTTPException(status_code=503, detail=err)

    employee.risk_score = result.probability
    employee.risk_level = result.risk_level
    db.commit()
    db.refresh(employee)
    return employee


@router.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
