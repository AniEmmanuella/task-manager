#Data models for the task manager

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class Task:
    """A single task with an optional due date."""

    id: int
    title: str
    due: date | None = None
    done: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert the task to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "due": self.due.isoformat() if self.due else None,
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        """Build a task from a dictionary loaded from JSON."""
        raw_due = data.get("due")
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            due=date.fromisoformat(raw_due) if raw_due else None,
            done=bool(data.get("done", False)),
        )