#!/bin/bash
# Sara's night shift: cron runs this at 23:00. Logs every night, and records ok or FAILED with the cost.
cd "$(dirname "$0")" || exit 1
mkdir -p logs
LOG="logs/$(date +%F).log"
if .venv/bin/python night_shift_safe.py "Start the night shift." >> "$LOG" 2>&1; then
    echo "$(date +%F) ok   $(grep -o '[0-9]* turns, \$[0-9.]*' "$LOG" | tail -1)" >> logs/nights.txt
else
    echo "$(date +%F) FAILED, see $LOG" >> logs/nights.txt
fi
tail -1 logs/nights.txt
