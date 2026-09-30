"""Command-line interface for the task manager."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from manager import (
    TaskFilter,
    TaskNotFoundError,
    add_task,
    complete_task,
    filter_tasks,
)
from models import Task
from storage import DEFAULT_PATH, StorageError, load_tasks, save_tasks


def parse_date(value: str) -> date:
    """Parse a YYYY-MM-DD string, for use as an argparse type."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{value}'. Use YYYY-MM-DD."
        ) from exc


def format_task(task: Task) -> str:
    """Return a one-line display string for a task."""
    mark = "[x]" if task.done else "[ ]"
    due = task.due.isoformat() if task.due else "no due date"
    return f"{task.id:>3} {mark} {task.title} (due: {due})"


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser with add, done and list commands."""
    parser = argparse.ArgumentParser(description="A simple task manager.")
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_PATH, help="Path to the tasks file."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("title", help="Task title.")
    add_parser.add_argument(
        "due", nargs="?", type=parse_date, default=None, help="Due date (YYYY-MM-DD)."
    )

    done_parser = subparsers.add_parser("done", help="Mark a task as done.")
    done_parser.add_argument("task_id", type=int, help="Id of the task.")

    list_parser = subparsers.add_parser("list", help="List tasks.")
    list_parser.add_argument(
        "filter",
        nargs="?",
        type=TaskFilter,
        choices=list(TaskFilter),
        default=TaskFilter.ALL,
        metavar="{all,done,pending}",
        help="Which tasks to show.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line app and return an exit code."""
    args = build_parser().parse_args(argv)
    try:
        tasks = load_tasks(args.file)
        if args.command == "add":
            task = add_task(tasks, args.title, args.due)
            save_tasks(tasks, args.file)
            print(f"Added task {task.id}.")
        elif args.command == "done":
            task = complete_task(tasks, args.task_id)
            save_tasks(tasks, args.file)
            print(f"Completed task {task.id}.")
        else:
            shown = filter_tasks(tasks, args.filter)
            if not shown:
                print("No tasks found.")
            for item in shown:
                print(format_task(item))
    except (StorageError, TaskNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())