"""Fixtures for HTTP + database integration tests."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def sqlite_database_url() -> Generator[str, None, None]:
    """Temporary SQLite file, ``DATABASE_URL``, and ``prisma db push`` for each test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db_path = Path(path).resolve()
    url = f"file:{db_path.as_posix()}"
    previous = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = url
    subprocess.run(
        [
            sys.executable,
            "-m",
            "prisma",
            "db",
            "push",
            "--skip-generate",
        ],
        cwd=str(PROJECT_ROOT),
        check=True,
        env={**os.environ},
    )
    try:
        yield url
    finally:
        if previous is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = previous
        db_path.unlink(missing_ok=True)


@pytest.fixture
def client(sqlite_database_url: str) -> Generator[TestClient, None, None]:
    """ASGI test client with Prisma connected to the temporary database."""
    _ = sqlite_database_url
    from taskmaster.presentation.main import app

    with TestClient(app) as test_client:
        yield test_client
