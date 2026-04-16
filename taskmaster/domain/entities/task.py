"""Task aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class TaskStatus(StrEnum):
    """Allowed values for task status (matches persisted string values)."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True, slots=True)
class Task:
    """Task entity.

    Attributes:
        id: Unique identifier (UUID string).
        title: Short title.
        description: Optional longer description.
        status: Current workflow status.
        created_at: Creation timestamp.
    """

    id: str
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
