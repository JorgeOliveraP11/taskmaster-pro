"""Standard API JSON envelope (see project .cursorrules)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorBody(BaseModel):
    """Error payload inside the envelope."""

    code: str
    message: str
    details: list[Any] | dict[str, Any] | None = None


class ApiEnvelope(BaseModel):
    """Unified success and error response shape."""

    success: bool
    data: Any = None
    error: ErrorBody | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


def success_envelope(data: Any, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a success response dict for JSONResponse.

    Args:
        data: Resource payload (object, list, or null).
        meta: Optional metadata (e.g. request id).

    Returns:
        Serializable body matching ``ApiEnvelope`` for successful calls.
    """
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": meta if meta is not None else {},
    }


def error_envelope(
    *,
    code: str,
    message: str,
    details: list[Any] | dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an error response dict for JSONResponse.

    Args:
        code: Machine-readable error code.
        message: Human-readable summary.
        details: Optional structured details (e.g. validation issues).
        meta: Optional metadata.

    Returns:
        Serializable body matching ``ApiEnvelope`` for failed calls.
    """
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "meta": meta if meta is not None else {},
    }
