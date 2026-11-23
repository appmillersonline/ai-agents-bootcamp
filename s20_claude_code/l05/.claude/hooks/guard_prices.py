"""PreToolUse hook: block any edit to prices.csv. Only Sara changes prices."""
import json
import sys

event = json.load(sys.stdin)                       # Claude Code sends the tool call as JSON
path = event["tool_input"].get("file_path", "")
if path.endswith("prices.csv"):
    print("prices.csv is changed only by Sara. Suggest the new price instead.", file=sys.stderr)
    sys.exit(2)                                    # exit code 2 = block, and tell Claude why
sys.exit(0)                                        # 0 = allow
