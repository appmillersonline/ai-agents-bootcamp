"""The shared to-do board: one SQLite file that every worker reads and writes, in any framework."""
import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "board.db"
OUTBOX = Path(__file__).parent / "outbox"
BRIEF = Path(__file__).parents[2] / "data" / "launch_brief.md"


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY, owner TEXT, title TEXT, file TEXT,
        status TEXT DEFAULT 'pending', note TEXT DEFAULT '')""")
    return con


def reset() -> None:
    DB.unlink(missing_ok=True)
    OUTBOX.mkdir(exist_ok=True)
    for f in OUTBOX.glob("*.md"):
        f.unlink()


def add_task(owner: str, title: str, file: str) -> int:
    with connect() as con:
        return con.execute("INSERT INTO tasks (owner, title, file) VALUES (?, ?, ?)", (owner, title, file)).lastrowid


def tasks() -> list[dict]:
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM tasks ORDER BY id")]


def task_for(owner: str) -> dict | None:
    with connect() as con:
        row = con.execute("SELECT * FROM tasks WHERE owner = ? AND status != 'done' ORDER BY id LIMIT 1", (owner,)).fetchone()
        return dict(row) if row else None


def set_status(task_id: int, status: str, note: str = "") -> None:
    with connect() as con:
        con.execute("UPDATE tasks SET status = ?, note = ? WHERE id = ?", (status, note, task_id))


def show() -> str:
    marks = {"pending": "[ ]", "working": "[~]", "done": "[x]", "redo": "[!]"}
    return "\n".join(f"  {marks.get(t['status'], '[?]')} #{t['id']} {t['owner']:<12} {t['title']}"
                     + (f"  ({t['note']})" if t["note"] else "") for t in tasks())
