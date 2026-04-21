"""Import all model modules so SQLAlchemy registers tables on Base.metadata."""

from app.models.employee import Employee  # noqa: F401
from app.models.intervention import Intervention  # noqa: F401

__all__ = ["Employee", "Intervention"]
