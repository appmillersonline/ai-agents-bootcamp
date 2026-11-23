"""Build dashboard.html from accounts.db: portfolio value per trader per day, and every trade with its reason."""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
COLORS = {"Mia": "#e76f51", "Vic": "#2a9d8f", "Cora": "#264653"}


def page(rows, trades) -> str:
    days = sorted({d for d, _, _ in rows})
    lo, hi = min(v for *_, v in rows) - 50, max(v for *_, v in rows) + 50
    x = lambda d: 60 + 520 * days.index(d) / max(1, len(days) - 1)
    y = lambda v: 260 - 220 * (v - lo) / (hi - lo)
    lines, used = "", []
    for t, c in sorted(COLORS.items(), key=lambda tc: -[v for d, n, v in rows if n == tc[0]][-1]):
        pts = [(d, v) for d, n, v in rows if n == t]
        lines += f'<polyline fill="none" stroke="{c}" stroke-width="4" points="{" ".join(f"{x(d):.0f},{y(v):.0f}" for d, v in pts)}"/>'
        ly = y(pts[-1][1]) + 5
        while any(abs(ly - u) < 20 for u in used):           # keep the end labels from overlapping
            ly += 20
        used.append(ly)
        lines += f'<text x="{x(pts[-1][0]) + 8:.0f}" y="{ly:.0f}" fill="{c}" font-weight="bold">{t} {pts[-1][1]:,.0f}</text>'
    axis = "".join(f'<text x="{x(d) - 14:.0f}" y="285" fill="#666">day {d}</text>' for d in days)
    table = "".join(f"<tr><td>{d}</td><td style='color:{COLORS[n]}'>{n}</td><td>{s} {q} {t}</td><td>{r}</td></tr>"
                    for d, n, s, t, q, r in trades)
    return f"""<html><body style="font-family:sans-serif;margin:30px;background:#faf8f3">
<h2>AI Trading Floor <span style="font-size:14px;color:#a00">simulated money, made-up companies</span></h2>
<svg width="720" height="300" style="background:white;border-radius:12px">
<line x1="60" x2="580" y1="{y(10000):.0f}" y2="{y(10000):.0f}" stroke="#ccc" stroke-dasharray="6"/>{lines}{axis}</svg>
<h3>Latest trades</h3><table cellpadding="6" style="background:white;border-radius:12px;font-size:14px">
<tr><th>day</th><th>trader</th><th>trade</th><th>reason</th></tr>{table}</table></body></html>"""


def build() -> str:
    con = sqlite3.connect(HERE / "accounts.db")
    rows = con.execute("SELECT day, trader, value FROM values_by_day ORDER BY day").fetchall()
    trades = con.execute("SELECT day, trader, side, ticker, shares, reason FROM trades ORDER BY rowid DESC LIMIT 8").fetchall()
    return page(rows, trades)


if __name__ == "__main__":
    (HERE / "dashboard.html").write_text(build())
    print("wrote dashboard.html")
