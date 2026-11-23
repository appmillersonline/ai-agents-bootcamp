"""The quality check, in plain code: a score you can measure, not a model's opinion."""
from agent_loop import board

LIMITS = {"card.md": 40}  # words; everything else may use up to 200


def check(task: dict) -> list[str]:
    path = board.OUTBOX / task["file"]
    if not path.exists():
        return ["file is missing"]
    text = path.read_text()
    problems = []
    if "lavender candle gift box" not in text.lower():
        problems.append("product name missing")
    if "29" not in text:
        problems.append("price missing")
    if text.count("!") > 1:
        problems.append(f"{text.count('!')} exclamation marks (max 1)")
    words, limit = len(text.split()), LIMITS.get(task["file"], 200)
    if words > limit:
        problems.append(f"{words} words (max {limit})")
    return problems
