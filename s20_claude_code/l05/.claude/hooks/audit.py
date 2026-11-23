"""PostToolUse hook: write one line per tool call to .claude/audit.log."""
import json
import sys
from datetime import datetime

event = json.load(sys.stdin)
detail = event["tool_input"].get("file_path") or event["tool_input"].get("command", "")
with open(".claude/audit.log", "a") as log:
    log.write(f"{datetime.now():%H:%M:%S} {event['tool_name']} {detail.split('/')[-1]}\n")
