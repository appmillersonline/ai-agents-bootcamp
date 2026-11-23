"""Read the local traces from the week and summarise them: tool calls, model calls, tokens and the slowest steps."""
import json
from collections import Counter
from pathlib import Path

spans = [json.loads(line) for line in open(Path(__file__).parent / "traces.jsonl")]
tools = Counter(s["data"]["name"] for s in spans if s["type"] == "function")
calls = [s for s in spans if s["type"] == "response"]
tokens_in = sum(s["data"]["usage"]["input_tokens"] for s in calls)
tokens_out = sum(s["data"]["usage"]["output_tokens"] for s in calls)

print(f"spans: {len(spans)}   model calls: {len(calls)}   tokens: {tokens_in:,} in, {tokens_out:,} out")
print("tool calls:", ", ".join(f"{name} {n}" for name, n in tools.most_common()))
slow = max(calls, key=lambda s: s["ms"] or 0)
print(f"slowest model call: {slow['ms'] / 1000:.1f} s   average: {sum(s['ms'] for s in calls) / len(calls) / 1000:.1f} s")
rejected = [s for s in spans if s["type"] == "function" and "Rejected" in str(s["data"].get("output"))]
print(f"rejected trades: {len(rejected)}")
for s in rejected:
    print(f"  {s['data']['input']} -> {str(s['data']['output']).split('Rejected: ')[1].rstrip("'}")[:70]}")
