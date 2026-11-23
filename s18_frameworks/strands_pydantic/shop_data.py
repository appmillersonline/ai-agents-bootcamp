"""Sara's stock list, shared by both demos (sample data)."""
import csv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[2] / ".env", override=True)
DATA = Path(__file__).parents[2] / "data"


def stock_rows() -> list[dict]:
    with open(DATA / "inventory.csv") as f:
        return [{"item": r["item"], "in_stock": int(r["in_stock"]), "reorder_at": int(r["reorder_at"])}
                for r in csv.DictReader(f)]
