"""Integration tests for task list API and status query parameter."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_get_tasks_status_filter_pending_and_completed(client: TestClient) -> None:
    """GET /tasks?status=... returns only tasks matching that status."""
    pending_only = client.post("/tasks", json={"title": "Stay pending", "description": None})
    to_complete = client.post("/tasks", json={"title": "Will complete", "description": None})
    assert pending_only.status_code == 201, pending_only.text
    assert to_complete.status_code == 201, to_complete.text

    completed_id = to_complete.json()["data"]["id"]
    patch = client.patch(f"/tasks/{completed_id}", json={"status": "COMPLETED"})
    assert patch.status_code == 200, patch.text

    pending_response = client.get("/tasks", params={"status": "PENDING"})
    assert pending_response.status_code == 200, pending_response.text
    pending_body = pending_response.json()
    assert pending_body["success"] is True
    assert pending_body["error"] is None
    pending_data = pending_body["data"]
    assert isinstance(pending_data, list)
    assert len(pending_data) == 1
    assert pending_data[0]["title"] == "Stay pending"
    assert pending_data[0]["status"] == "PENDING"

    completed_response = client.get("/tasks", params={"status": "COMPLETED"})
    assert completed_response.status_code == 200, completed_response.text
    completed_body = completed_response.json()
    assert completed_body["success"] is True
    completed_data = completed_body["data"]
    assert isinstance(completed_data, list)
    assert len(completed_data) == 1
    assert completed_data[0]["title"] == "Will complete"
    assert completed_data[0]["status"] == "COMPLETED"
