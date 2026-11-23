"""Sara's sales database as an MCP server: look at the tables, run read-only SQL, draw a bar chart."""
import re
import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP

HERE = Path(__file__).parent
DB = f"file:{HERE / 'sales.db'}?mode=ro"          # read-only: the database itself refuses writes
mcp = FastMCP("sara-sales", log_level="WARNING")


@mcp.tool()
def describe_tables() -> str:
    """Show every table and its columns. Call this first, before writing any SQL."""
    con = sqlite3.connect(DB, uri=True)
    return "\n".join(row[0] for row in con.execute("SELECT sql FROM sqlite_master WHERE type='table'"))


@mcp.tool()
def run_sql(query: str) -> str:
    """Run one read-only SQL query (SELECT or WITH) on the sales database. Returns at most 50 rows.

    Args:
        query: For example "SELECT name, price_eur FROM products".
    """
    if not re.match(r"\s*(select|with)\b", query, re.I):
        return "Only SELECT queries are allowed."
    con = sqlite3.connect(DB, uri=True)
    try:
        cur = con.execute(query)
    except sqlite3.Error as e:
        return f"SQL error: {e}"
    cols = [d[0] for d in cur.description]
    rows = cur.fetchmany(50)
    return "\n".join([" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows])


@mcp.tool()
def bar_chart(title: str, labels: list[str], values: list[float]) -> str:
    """Draw a bar chart for Sara. Saves an SVG in charts/ and returns a text version.

    Args:
        title: Short title, for example "Revenue by month".
        labels: One label per bar.
        values: One number per bar, same order as labels.
    """
    top = max(values) or 1
    lines = [title] + [f"{label[:16]:<16} {'█' * round(30 * v / top):<30} {v:,.2f}" for label, v in zip(labels, values)]
    bars = "".join(f'<rect x="10" y="{30 + i * 30}" width="{400 * v / top:.0f}" height="22" fill="#2a9d8f"/>'
                   f'<text x="15" y="{46 + i * 30}" font-size="13" fill="white">{label}: {v:,.2f}</text>'
                   for i, (label, v) in enumerate(zip(labels, values)))
    (HERE / "charts").mkdir(exist_ok=True)
    name = re.sub(r"\W+", "_", title.lower()).strip("_")
    (HERE / "charts" / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="{40 + 30 * len(values)}">'
        f'<text x="10" y="20" font-size="15">{title}</text>{bars}</svg>')
    return "\n".join(lines) + f"\n(saved charts/{name}.svg)"


if __name__ == "__main__":
    mcp.run()
