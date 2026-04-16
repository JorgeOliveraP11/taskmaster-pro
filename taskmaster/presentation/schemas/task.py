"""Task-related request and response models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from taskmaster.domain.entities.task import TaskStatus


class TaskCreateRequest(BaseModel):
    """Body for creating a task."""

    title: str = Field(min_length=1, max_length=2000)
    description: str | None = None


class TaskUpdateRequest(BaseModel):
    """Body for partially updating a task (PATCH)."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

    @field_validator("title")
    @classmethod
    def validate_title_when_set(cls, value: str | None) -> str | None:
        """Reject empty strings; trim whitespace."""
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be empty when provided")
        if len(stripped) > 2000:
            raise ValueError("title is too long")
        return stripped


class TaskResponse(BaseModel):
    """Task serialized for API ``data`` payloads."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime = Field(serialization_alias="createdAt")

    @field_validator("status", mode="before")
    @classmethod
    def coerce_status(cls, value: TaskStatus | str) -> TaskStatus:
        """Allow construction from domain entity or raw string."""
        if isinstance(value, TaskStatus):
            return value
        return TaskStatus(value)
