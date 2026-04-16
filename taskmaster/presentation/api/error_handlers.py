"""Map exceptions to the standard JSON envelope."""

from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from taskmaster.domain.errors import TaskNotFoundError
from taskmaster.presentation.schemas.envelope import error_envelope


async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    """Return 404 with ``NOT_FOUND`` when a task is missing."""
    _ = request
    return JSONResponse(
        status_code=404,
        content=error_envelope(
            code="NOT_FOUND",
            message=str(exc),
            details={"task_id": exc.task_id},
        ),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return 422 with ``VALIDATION_ERROR`` for request body/query issues."""
    _ = request
    return JSONResponse(
        status_code=422,
        content=error_envelope(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=exc.errors(),
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Normalize FastAPI/Starlette HTTPException responses to the standard envelope."""
    _ = request
    detail = exc.detail
    message = detail if isinstance(detail, str) else "Request failed"
    details: object | None = None if isinstance(detail, str) else detail
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content=error_envelope(
                code="NOT_FOUND",
                message=message,
                details=details,
            ),
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_envelope(
            code=f"HTTP_{exc.status_code}",
            message=message,
            details=details,
        ),
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Map business rule violations (e.g. empty PATCH) to 422."""
    _ = request
    return JSONResponse(
        status_code=422,
        content=error_envelope(
            code="VALIDATION_ERROR",
            message=str(exc),
            details=None,
        ),
    )
