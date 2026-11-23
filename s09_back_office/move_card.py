"""Nadia has started the photos: move her card to 'Doing' and draw the board again. Plain code, no AI."""
import json
import sys

import task_board_lib as board

who, column = sys.argv[1], sys.argv[2]  # for example: Nadia Doing
cards = json.loads(board.BOARD.read_text())
for card in cards:
    if card["owner"] == who and card["column"] != "Done":
        card["column"] = column
        print(f"Moved to {column}: {card['title']}")
        break
board.BOARD.write_text(json.dumps(cards, indent=1))
board.draw_board()
