"""Run Claude Code headless every morning: check today's orders and save a JSON report."""
import json
import subprocess
from datetime import date

PROMPT = """Check orders_today.csv for problems: duplicate order ids, unusual quantities,
and prices that don't match prices.csv. Reply with only JSON, no other text:
{"ok": true or false, "issues": ["one short sentence per problem"]}"""

cmd = ["claude", "-p", PROMPT, "--output-format", "json", "--allowedTools", "Read", "--max-turns", "5"]
run = json.loads(subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout)

answer = run["result"].strip().removeprefix("```json").removesuffix("```")
report = json.loads(answer)                      # the model's own JSON
report.update(date=str(date.today()), cost_usd=round(run["total_cost_usd"], 3), session=run["session_id"])
with open("daily_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"ok: {report['ok']}  ({len(report['issues'])} issues, ${report['cost_usd']})")
for issue in report["issues"]:
    print(f"  - {issue}")
print(f"session: {report['session'][:8]}...")
