"""Core task operations, independent of storage and the command line."""

from __future__ import annotations

from datetime import date
from enum import Enum

from models import Task


class TaskFilter(str, Enum):
    """Which tasks to show when listing."""

    ALL = "all"
    DONE = "done"
    PENDING = "pending"


class TaskNotFoundError(Exception):
    """Raised when no task matches the given id."""


def next_id(tasks: list[Task]) -> int:
    """Return an id one higher than the current maximum, so ids are never reused."""
    return max((task.id for task in tasks), default=0) + 1


def add_task(tasks: list[Task], title: str, due: date | None = None) -> Task:
    """Create a task, append it to the list, and return it."""
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Task title cannot be empty.")
    task = Task(id=next_id(tasks), title=cleaned, due=due)
    tasks.append(task)
    return task


def complete_task(tasks: list[Task], task_id: int) -> Task:
    """Mark the task with the given id as done and return it."""
    for task in tasks:
        if task.id == task_id:
            task.done = True
            return task
    raise TaskNotFoundError(f"No task with id {task_id}.")


def filter_tasks(
    tasks: list[Task], task_filter: TaskFilter = TaskFilter.ALL
) -> list[Task]:
    """Return tasks matching the filter."""
    if task_filter is TaskFilter.DONE:
        return [task for task in tasks if task.done]
    if task_filter is TaskFilter.PENDING:
        return [task for task in tasks if not task.done]
    return list(tasks)