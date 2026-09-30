"""Tests for the core task operations."""

from datetime import date

import pytest

from manager import (
    TaskFilter,
    TaskNotFoundError,
    add_task,
    complete_task,
    filter_tasks,
    next_id,
)
from models import Task


def test_next_id_empty_list() -> None:
    assert next_id([]) == 1


def test_next_id_never_reuses_ids() -> None:
    tasks = [Task(id=1, title="a"), Task(id=5, title="b")]
    assert next_id(tasks) == 6


def test_add_task_appends_and_returns_task() -> None:
    tasks: list[Task] = []
    task = add_task(tasks, "  Buy milk  ", date(2026, 10, 5))
    assert tasks == [task]
    assert task.title == "Buy milk"
    assert task.due == date(2026, 10, 5)
    assert task.done is False


def test_add_task_rejects_empty_title() -> None:
    with pytest.raises(ValueError):
        add_task([], "   ")


def test_complete_task_marks_done() -> None:
    tasks = [Task(id=1, title="a")]
    complete_task(tasks, 1)
    assert tasks[0].done is True


def test_complete_task_unknown_id_raises() -> None:
    with pytest.raises(TaskNotFoundError):
        complete_task([], 99)


def test_filter_tasks() -> None:
    tasks = [Task(id=1, title="a", done=True), Task(id=2, title="b")]
    assert [t.id for t in filter_tasks(tasks, TaskFilter.DONE)] == [1]
    assert [t.id for t in filter_tasks(tasks, TaskFilter.PENDING)] == [2]
    assert len(filter_tasks(tasks)) == 2