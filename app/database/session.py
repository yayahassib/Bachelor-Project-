"""SQLite engine and session factory."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Project root: .../app/database/session.py -> parents[2] is bachelor 3/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "turnover.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# check_same_thread=False is required when SQLite is used with FastAPI (multiple threads)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency: yields one database session per request."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
