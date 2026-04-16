"""Prisma-backed task repository."""

from __future__ import annotations

from typing import Any

from prisma import Prisma
from prisma.models import Task as PrismaTask

from taskmaster.domain.entities.task import Task, TaskStatus
from taskmaster.domain.errors import TaskNotFoundError
from taskmaster.domain.repositories.task_repository import TaskRepository
from taskmaster.domain.value_objects.partial_task_update import PartialTaskUpdate, _MISSING


class PrismaTaskRepository(TaskRepository):
    """Maps between Prisma records and domain ``Task`` entities."""

    def __init__(self, client: Prisma) -> None:
        self._db = client

    def _to_entity(self, record: PrismaTask) -> Task:
        return Task(
            id=record.id,
            title=record.title,
            description=record.description,
            status=TaskStatus(record.status),
            created_at=record.createdAt,
        )

    async def create(self, title: str, description: str | None) -> Task:
        record = await self._db.task.create(
            data={
                "title": title,
                "description": description,
            }
        )
        return self._to_entity(record)

    async def get_by_id(self, task_id: str) -> Task:
        record = await self._db.task.find_unique(where={"id": task_id})
        if record is None:
            raise TaskNotFoundError(task_id)
        return self._to_entity(record)

    async def list_all(self) -> list[Task]:
        records = await self._db.task.find_many()
        return [self._to_entity(r) for r in records]

    async def filter_by_status(self, status: TaskStatus) -> list[Task]:
        records = await self._db.task.find_many(where={"status": status.value})
        return [self._to_entity(r) for r in records]

    async def update(self, task_id: str, patch: PartialTaskUpdate) -> Task:
        data: dict[str, Any] = {}
        if patch.title is not _MISSING:
            data["title"] = patch.title
        if patch.description is not _MISSING:
            data["description"] = patch.description
        if patch.status is not _MISSING:
            data["status"] = patch.status.value

        record = await self._db.task.update(where={"id": task_id}, data=data)
        if record is None:
            raise TaskNotFoundError(task_id)
        return self._to_entity(record)

    async def delete(self, task_id: str) -> None:
        record = await self._db.task.delete(where={"id": task_id})
        if record is None:
            raise TaskNotFoundError(task_id)
