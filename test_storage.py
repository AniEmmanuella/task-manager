"""Tests for JSON file storage."""

from datetime import date
from pathlib import Path

import pytest

from models import Task
from storage import StorageError, load_tasks, save_tasks


def test_load_missing_file_returns_empty_list(tmp_path: Path) -> None:
    assert load_tasks(tmp_path / "missing.json") == []


def test_save_then_load_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    tasks = [
        Task(id=1, title="a", due=date(2026, 10, 5)),
        Task(id=2, title="b", done=True),
    ]
    save_tasks(tasks, path)
    assert load_tasks(path) == tasks


def test_load_corrupted_json_raises(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(StorageError):
        load_tasks(path)


def test_load_missing_field_raises(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    path.write_text('[{"id": 1}]', encoding="utf-8")
    with pytest.raises(StorageError):
        load_tasks(path)