"""Save a copy of the live page with the backend's current data inside it, so it can be pictured offline."""
import json
from pathlib import Path

import httpx

page = httpx.get("http://127.0.0.1:8023/").text
data = httpx.get("http://127.0.0.1:8023/api/floor").json()
fake_fetch = f"const data = {json.dumps(data)};"
page = page.replace('const data = await (await fetch("/api/floor")).json();', fake_fetch)
Path(__file__).with_name("app_snapshot.html").write_text(page)
print(f"saved app_snapshot.html with {len(data['history'])} values and {len(data['trades'])} trades")
