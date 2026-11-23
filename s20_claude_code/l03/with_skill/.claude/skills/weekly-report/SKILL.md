---
name: weekly-report
description: Write Sara's weekly sales report from orders.csv. Use when asked for a weekly report, a sales summary, or how the shop did this week.
---

# Weekly sales report

1. Get the numbers by running `python .claude/skills/weekly-report/summary.py orders.csv`. Never add up the numbers yourself.
2. Write `report.md` with exactly three sections:
   - `## Numbers` (revenue, orders, items sold)
   - `## Best seller`
   - `## One thing to do next week`
3. Keep it under 120 words. Money in euros with two decimals.
4. Reply with one line: where the report is and the revenue.
