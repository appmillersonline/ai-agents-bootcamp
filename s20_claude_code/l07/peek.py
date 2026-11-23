"""Print the important fields of a `claude -p --output-format json` result."""
import json
import sys

run = json.load(sys.stdin)
print(f"stopped: {run['subtype']} | error: {run['is_error']} | turns: {run['num_turns']} | cost: ${run['total_cost_usd']:.3f}")
