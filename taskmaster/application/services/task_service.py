"""Task use cases."""

from __future__ import annotations

from taskmaster.domain.entities.task import Task, TaskStatus
from taskmaster.domain.repositories.task_repository import TaskRepository
from taskmaster.domain.value_objects.partial_task_update import PartialTaskUpdate


class TaskService:
    """Coordinates task CRUD and queries."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def create_task(self, title: str, description: str | None) -> Task:
        """Create a task with default status PENDING.

        Args:
            title: Non-empty title.
            description: Optional body text.

        Returns:
            The persisted task.
        """
        return await self._repository.create(title=title, description=description)

    async def get_task(self, task_id: str) -> Task:
        """Return a single task by id.

        Args:
            task_id: Task primary key.

        Returns:
            The task if found.

        Raises:
            TaskNotFoundError: If the task does not exist.
        """
        return await self._repository.get_by_id(task_id)

    async def list_tasks(self) -> list[Task]:
        """Return all tasks."""
        return await self._repository.list_all()

    async def filter_by_status(self, status: TaskStatus) -> list[Task]:
        """Return tasks with the given status.

        Args:
            status: Status filter.

        Returns:
            Matching tasks (possibly empty).
        """
        return await self._repository.filter_by_status(status)

    async def update_task(self, task_id: str, patch: PartialTaskUpdate) -> Task:
        """Apply a partial update.

        Args:
            task_id: Task primary key.
            patch: Fields to change; omitted fields stay unchanged.

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If the task does not exist.
            ValueError: If no fields are provided to update.
        """
        if not patch.has_changes():
            raise ValueError("At least one field must be provided to update a task")

        return await self._repository.update(task_id, patch)

    async def delete_task(self, task_id: str) -> None:
        """Delete a task by id.

        Args:
            task_id: Task primary key.

        Raises:
            TaskNotFoundError: If the task does not exist.
        """
        await self._repository.delete(task_id)
