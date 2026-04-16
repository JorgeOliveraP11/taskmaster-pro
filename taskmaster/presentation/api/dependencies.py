"""FastAPI dependency providers."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from prisma import Prisma

from taskmaster.application.services.task_service import TaskService
from taskmaster.domain.repositories.task_repository import TaskRepository
from taskmaster.infrastructure.persistence.prisma_task_repository import PrismaTaskRepository


def get_prisma(request: Request) -> Prisma:
    """Return the shared Prisma client from application state.

    Args:
        request: Current HTTP request.

    Returns:
        Connected Prisma client.

    Raises:
        RuntimeError: If lifespan has not attached a client.
    """
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise RuntimeError("Prisma client is not available on application state")
    return db


def get_task_repository(
    db: Annotated[Prisma, Depends(get_prisma)],
) -> TaskRepository:
    """Construct the task repository adapter."""
    return PrismaTaskRepository(db)


def get_task_service(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
) -> TaskService:
    """Construct the task application service."""
    return TaskService(repository)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
