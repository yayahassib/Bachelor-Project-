"""Central API error handling (beginner-friendly messages)."""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app")


async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    logger.exception("Database error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database error occurred. Check server logs or try again.",
        },
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
