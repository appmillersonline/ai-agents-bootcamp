"""Project 10 tests: the account rules (no model needed), and a check of what the traders really did."""
import os
import sqlite3
import tempfile
from pathlib import Path

os.environ["MARKET_DAY"] = "30"
import accounts  # noqa: E402

REAL_DB = accounts.DB


def fresh(name="Test"):
    accounts.DB = Path(tempfile.mkdtemp()) / "test.db"          # never touch the real accounts
    accounts.open_account(name)
    return name


def test_cannot_overspend():
    t = fresh()
    assert accounts.trade(t, "buy", "TIDE", 1000, "too much").startswith("Rejected")


def test_thirty_percent_cap():
    t = fresh()
    assert "30%" in accounts.trade(t, "buy", "NOVA", 200, "all in on one")


def test_cannot_sell_what_you_dont_own():
    t = fresh()
    assert accounts.trade(t, "sell", "CLAY", 5, "short").startswith("Rejected")


def test_cora_cash_rule_is_enforced():
    t = fresh("Cora")
    assert accounts.trade(t, "buy", "TIDE", 50, "fine").startswith("Done")       # about 25% of her money
    assert "keep 50%" in accounts.trade(t, "buy", "WICK", 90, "too much")      # would leave under half in cash


def test_cora_keeps_half_in_cash():
    con = sqlite3.connect(REAL_DB)                                # what really happened this week
    cash = con.execute("SELECT amount FROM cash WHERE trader = 'Cora'").fetchone()[0]
    accounts.DB = REAL_DB
    value = accounts.portfolio("Cora")["value"]
    assert cash >= 0.5 * value, f"Cora has only {100 * cash / value:.0f}% in cash"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as e:
                print(f"FAIL  {name}: {e}")
