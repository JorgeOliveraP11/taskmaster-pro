"""Value object for a partial task update (patch semantics)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from taskmaster.domain.entities.task import TaskStatus

_MISSING: Any = object()


@dataclass(frozen=True, slots=True)
class PartialTaskUpdate:
    """Omitted attributes mean \"leave unchanged\" (not same as setting to ``None``)."""

    title: str | Any = _MISSING
    description: str | None | Any = _MISSING
    status: TaskStatus | Any = _MISSING

    def has_changes(self) -> bool:
        """Return True if at least one field is explicitly set."""
        if self.title is not _MISSING:
            return True
        if self.description is not _MISSING:
            return True
        if self.status is not _MISSING:
            return True
        return False

    @staticmethod
    def from_mapping(data: dict[str, Any]) -> PartialTaskUpdate:
        """Build from a dict that only contains keys the client sent.

        Args:
            data: Keys are a subset of title, description, status.

        Returns:
            PartialTaskUpdate with :data:`_MISSING` for absent keys.
        """
        return PartialTaskUpdate(
            title=data["title"] if "title" in data else _MISSING,
            description=data["description"] if "description" in data else _MISSING,
            status=TaskStatus(data["status"]) if "status" in data else _MISSING,
        )
