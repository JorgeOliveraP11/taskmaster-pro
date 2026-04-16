"""Domain-level exceptions."""


class TaskNotFoundError(Exception):
    """Raised when a task does not exist for the given identifier."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id '{task_id}' was not found")
