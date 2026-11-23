"""Meeting-notes agent: the team's task board (load, add, draw) and phone pings, shared by task_board.py and move_card.py."""
import html
import json
import os
from pathlib import Path

import requests

DATA = Path(__file__).parent.parent / "data"
BOARD = DATA / "board.json"


def load_board():
    return json.loads(BOARD.read_text()) if BOARD.exists() else []


def add_to_board(task, meeting):
    board = load_board()
    board.append({**task.model_dump(), "column": "To do", "meeting": meeting})
    BOARD.write_text(json.dumps(board, indent=1))


def notify(text):
    requests.post(f"https://ntfy.sh/{os.getenv('NTFY_TOPIC')}", data=text.encode("utf-8"))  # the same phone ping as in Start Here


def draw_board():
    board = json.loads(BOARD.read_text())
    columns = ""
    for name in ["To do", "Doing", "Done"]:
        cards = "".join(f"<div class='card {c['priority']}'><b>{html.escape(c['title'])}</b>"
                        f"<span>{c['owner']} · {c['due'] or 'no date'}</span></div>"
                        for c in board if c["column"] == name)
        columns += f"<div class='col'><h2>{name}</h2>{cards}</div>"
    style = ("body{font-family:Helvetica;background:#f3f1ec;margin:30px}.cols{display:flex;gap:24px}"
             ".col{flex:1;background:#e6e2d9;border-radius:14px;padding:16px}.card{background:#fff;border-radius:10px;"
             "padding:14px;margin:12px 0;border-left:8px solid #8fb8de}.card.high{border-left-color:#e3735e}"
             ".card span{display:block;color:#666;margin-top:6px}")
    (DATA / "task_board.html").write_text(f"<html><meta charset='utf-8'><style>{style}</style><h1>Sara's Shop: team board</h1>"
                                          f"<div class='cols'>{columns}</div></html>")
