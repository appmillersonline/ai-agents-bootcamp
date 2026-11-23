#!/bin/bash
# Run five simulated trading days, one session per day (fake money, made-up market).
cd "$(dirname "$0")/.." || exit 1
for day in 26 27 28 29 30; do
    uv run python s23_trading_floor/floor.py $day 2>&1 | grep "^== day"
done
MARKET_DAY=30 uv run python s23_trading_floor/report.py
