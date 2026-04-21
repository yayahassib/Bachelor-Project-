import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
import app.models  # noqa: F401 - registers ORM models with Base.metadata
from app.error_handlers import register_exception_handlers
from app.routes import employees, interventions, prediction

logging.basicConfig(level=logging.INFO)

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Early Turnover Prediction System",
    description="API for predicting employee turnover early.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(interventions.router)
app.include_router(prediction.router)

register_exception_handlers(app)


@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}


@app.get("/")
def serve_index():
    """Serve the main frontend page when ``frontend/index.html`` exists."""
    index = FRONTEND_DIR / "index.html"
    if index.is_file():
        return FileResponse(index)
    return {
        "message": "API is running",
        "hint": "Add frontend/index.html to see the UI at this URL.",
        "health": "/health",
        "docs": "/docs",
    }


@app.get("/dashboard")
def serve_dashboard():
    path = FRONTEND_DIR / "dashboard.html"
    if not path.is_file():
        return JSONResponse(
            status_code=404,
            content={"detail": "dashboard.html not found in frontend/"},
        )
    return FileResponse(path)


@app.get("/employee")
def serve_employee_page():
    path = FRONTEND_DIR / "employee.html"
    if not path.is_file():
        return JSONResponse(
            status_code=404,
            content={"detail": "employee.html not found in frontend/"},
        )
    return FileResponse(path)


app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static",
)
