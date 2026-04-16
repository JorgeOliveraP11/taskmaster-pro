"""Abstract task persistence port."""

from __future__ import annotations

from abc import ABC, abstractmethod

from taskmaster.domain.entities.task import Task, TaskStatus
from taskmaster.domain.value_objects.partial_task_update import PartialTaskUpdate


class TaskRepository(ABC):
    """Persistence abstraction for tasks.

    Implementations live in the infrastructure layer (e.g. Prisma).
    """

    @abstractmethod
    async def create(self, title: str, description: str | None) -> Task:
        """Persist a new task with default status PENDING."""

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Task:
        """Return a task by id.

        Raises:
            TaskNotFoundError: If no task exists for the id.
        """

    @abstractmethod
    async def list_all(self) -> list[Task]:
        """Return all tasks (no guaranteed order)."""

    @abstractmethod
    async def filter_by_status(self, status: TaskStatus) -> list[Task]:
        """Return tasks matching the given status."""

    @abstractmethod
    async def update(self, task_id: str, patch: PartialTaskUpdate) -> Task:
        """Apply partial updates; omitted patch fields are left unchanged.

        Raises:
            TaskNotFoundError: If no task exists for the id.
        """

    @abstractmethod
    async def delete(self, task_id: str) -> None:
        """Remove a task by id.

        Raises:
            TaskNotFoundError: If no task exists for the id.
        """
