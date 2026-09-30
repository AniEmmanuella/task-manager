# Task Manager

A command-line task manager in Python. Refactored from a single untyped script into typed, tested modules.

## Usage

    python task_manager.py add "Write report" 2026-10-10
    python task_manager.py done 1
    python task_manager.py list [all|done|pending]

## Style report

| Check | Before | After |
|-------|--------|-------|
| ruff (E, F, N, I, B, UP) | 10 errors | 0 errors |
| mypy --strict | 14 errors | 0 errors |
| pytest | no tests | 11 passing |

The raw tool output is in `style_before.txt`, `types_before.txt`, `style_after.txt`, `types_after.txt` and `tests_after.txt`.

## Rationale for key changes

1. **Split one file into modules.** `models.py` holds the data, `storage.py` handles the file, `manager.py` holds the logic, and `task_manager.py` is only the CLI. This makes each part testable on its own.
2. **Added type hints and a `Task` dataclass.** Tasks were untyped dictionaries before. A dataclass catches typos in field names and lets mypy check every function.
3. **Real dates.** Due dates were plain strings. They are now `date` objects, and invalid dates are rejected with a clear message.
4. **Safer ids.** The old code used `len(tasks) + 1`, which could repeat an id after a deletion. `next_id` uses the current maximum instead.
5. **Error handling.** Corrupted files, unknown ids, empty titles and bad dates now give a clean error and exit code 1 instead of a traceback.
6. **`argparse` instead of manual `sys.argv` parsing.** This gives automatic `--help`, validation and usage messages.
7. **Tests.** `pytest` covers the core logic and storage, including the failure cases.