from datetime import date

from pydantic import BaseModel, ConfigDict


class InterventionCreate(BaseModel):
    """Fields sent when creating an intervention (same as the table, without `id`)."""

    employee_id: int
    intervention_type: str
    notes: str = ""
    date_applied: date


class InterventionResponse(BaseModel):
    """Intervention as returned by the API (includes database `id`)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    intervention_type: str
    notes: str
    date_applied: date
