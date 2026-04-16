"""Task HTTP routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from taskmaster.domain.entities.task import TaskStatus
from taskmaster.domain.value_objects.partial_task_update import PartialTaskUpdate
from taskmaster.presentation.api.dependencies import TaskServiceDep
from taskmaster.presentation.schemas.envelope import success_envelope
from taskmaster.presentation.schemas.task import TaskCreateRequest, TaskResponse, TaskUpdateRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _task_to_json(task: TaskResponse) -> dict[str, object]:
    return task.model_dump(mode="json", by_alias=True)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreateRequest,
    service: TaskServiceDep,
) -> JSONResponse:
    """Create a new task."""
    task = await service.create_task(title=body.title, description=body.description)
    payload = TaskResponse.model_validate(task, from_attributes=True)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=success_envelope(_task_to_json(payload)),
    )


@router.get("")
async def list_tasks(
    service: TaskServiceDep,
    status_filter: Annotated[TaskStatus | None, Query(alias="status")] = None,
) -> JSONResponse:
    """List tasks, optionally filtered by status."""
    if status_filter is not None:
        tasks = await service.filter_by_status(status_filter)
    else:
        tasks = await service.list_tasks()
    data = [
        _task_to_json(TaskResponse.model_validate(t, from_attributes=True)) for t in tasks
    ]
    return JSONResponse(content=success_envelope(data))


@router.get("/{task_id}")
async def get_task(task_id: str, service: TaskServiceDep) -> JSONResponse:
    """Get a single task by id."""
    task = await service.get_task(task_id)
    payload = TaskResponse.model_validate(task, from_attributes=True)
    return JSONResponse(content=success_envelope(_task_to_json(payload)))


@router.patch("/{task_id}")
async def update_task(
    task_id: str,
    body: TaskUpdateRequest,
    service: TaskServiceDep,
) -> JSONResponse:
    """Apply a partial update to a task."""
    patch = PartialTaskUpdate.from_mapping(body.model_dump(exclude_unset=True))
    task = await service.update_task(task_id, patch)
    payload = TaskResponse.model_validate(task, from_attributes=True)
    return JSONResponse(content=success_envelope(_task_to_json(payload)))


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: str, service: TaskServiceDep) -> JSONResponse:
    """Delete a task (response uses the standard JSON envelope; body has null data)."""
    await service.delete_task(task_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=success_envelope(None))
