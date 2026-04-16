"""Unit tests for ``TaskService`` with a mocked ``TaskRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from taskmaster.application.services.task_service import TaskService
from taskmaster.domain.entities.task import Task, TaskStatus
from taskmaster.domain.errors import TaskNotFoundError
from taskmaster.domain.repositories.task_repository import TaskRepository
from taskmaster.domain.value_objects.partial_task_update import PartialTaskUpdate


def _sample_task(
    *,
    task_id: str = "550e8400-e29b-41d4-a716-446655440000",
    status: TaskStatus = TaskStatus.PENDING,
) -> Task:
    return Task(
        id=task_id,
        title="Sample",
        description="desc",
        status=status,
        created_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def mock_repository() -> AsyncMock:
    """Async mock implementing the repository port."""
    return AsyncMock(spec=TaskRepository)


@pytest.fixture
def task_service(mock_repository: AsyncMock) -> TaskService:
    return TaskService(mock_repository)


@pytest.mark.asyncio
async def test_create_task_delegates_to_repository(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    expected = _sample_task()
    mock_repository.create.return_value = expected

    result = await task_service.create_task(title="Sample", description="desc")

    assert result is expected
    mock_repository.create.assert_awaited_once_with(title="Sample", description="desc")


@pytest.mark.asyncio
async def test_get_task_delegates_to_repository(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    expected = _sample_task()
    mock_repository.get_by_id.return_value = expected

    result = await task_service.get_task("550e8400-e29b-41d4-a716-446655440000")

    assert result is expected
    mock_repository.get_by_id.assert_awaited_once_with("550e8400-e29b-41d4-a716-446655440000")


@pytest.mark.asyncio
async def test_get_task_propagates_not_found(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_by_id.side_effect = TaskNotFoundError("missing-id")

    with pytest.raises(TaskNotFoundError):
        await task_service.get_task("missing-id")


@pytest.mark.asyncio
async def test_list_tasks_delegates_to_repository(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    tasks = [_sample_task(task_id="a"), _sample_task(task_id="b")]
    mock_repository.list_all.return_value = tasks

    result = await task_service.list_tasks()

    assert result == tasks
    mock_repository.list_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_filter_by_status_delegates_with_status(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    tasks = [_sample_task(status=TaskStatus.COMPLETED)]
    mock_repository.filter_by_status.return_value = tasks

    result = await task_service.filter_by_status(TaskStatus.COMPLETED)

    assert result == tasks
    mock_repository.filter_by_status.assert_awaited_once_with(TaskStatus.COMPLETED)


@pytest.mark.asyncio
async def test_update_task_raises_when_patch_is_empty(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    patch = PartialTaskUpdate()

    with pytest.raises(ValueError, match="At least one field"):
        await task_service.update_task("any-id", patch)

    mock_repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_task_delegates_to_repository(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    patch = PartialTaskUpdate.from_mapping({"title": "New title"})
    updated = _sample_task()
    mock_repository.update.return_value = updated

    result = await task_service.update_task("tid", patch)

    assert result is updated
    mock_repository.update.assert_awaited_once_with("tid", patch)


@pytest.mark.asyncio
async def test_delete_task_delegates_to_repository(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.delete.return_value = None

    await task_service.delete_task("to-delete")

    mock_repository.delete.assert_awaited_once_with("to-delete")


@pytest.mark.asyncio
async def test_delete_task_propagates_not_found(
    task_service: TaskService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.delete.side_effect = TaskNotFoundError("gone")

    with pytest.raises(TaskNotFoundError):
        await task_service.delete_task("gone")
