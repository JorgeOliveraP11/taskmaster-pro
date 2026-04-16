"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from prisma import Prisma

from taskmaster.domain.errors import TaskNotFoundError
from taskmaster.presentation.api.error_handlers import (
    http_exception_handler,
    task_not_found_handler,
    validation_exception_handler,
    value_error_handler,
)
from taskmaster.presentation.api.routes.tasks import router as tasks_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Connect Prisma on startup and disconnect on shutdown."""
    db = Prisma()
    await db.connect()
    app.state.db = db
    yield
    await db.disconnect()


app = FastAPI(title="Taskmaster Pro", lifespan=lifespan)

app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)

app.include_router(tasks_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Liveness probe (minimal JSON; not wrapped in the task API envelope)."""
    return {"status": "ok"}
