#JSON file storage for tasks

from __future__ import annotations

import json
from pathlib import Path

from models import Task

DEFAULT_PATH = Path("tasks.json")


class StorageError(Exception):
    """Raised when the task file cannot be read."""


def load_tasks(path: Path = DEFAULT_PATH) -> list[Task]:
    """Load all tasks from a JSON file, returning an empty list if it is missing."""
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [Task.from_dict(item) for item in raw]
    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        raise StorageError(f"Could not read {path}: {exc}") from exc


def save_tasks(tasks: list[Task], path: Path = DEFAULT_PATH) -> None:
    """Write all tasks to a JSON file."""
    data = [task.to_dict() for task in tasks]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")