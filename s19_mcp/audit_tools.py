"""Audit an MCP server before you trust it: read every tool, flag red flags, pin what you approved."""
import asyncio
import hashlib
import json
import re
import sys
from pathlib import Path

from agents.mcp import MCPServerStdio

HERE = Path(__file__).parent
PINS = HERE / "safety" / "tool_pins.json"
RED_FLAGS = r"ignore (all|previous)|do not (mention|tell)|before (calling|using)|password|secret|pin\b|\.env|ssh|<important>"


async def audit(name: str, params: dict) -> None:
    async with MCPServerStdio(name=name, params=params, client_session_timeout_seconds=30) as server:
        tools = await server.list_tools()
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    print(f"== {name}: {len(tools)} tool(s)")
    for t in tools:
        text = (t.description or "") + json.dumps(t.inputSchema, sort_keys=True)
        fingerprint = hashlib.sha256(text.encode()).hexdigest()[:12]
        flags = sorted({m.group(0).lower() for m in re.finditer(RED_FLAGS, text, re.I)})
        key = f"{name}/{t.name}"
        status = "new" if key not in pins else ("same as approved" if pins[key] == fingerprint else "CHANGED since you approved it")
        print(f"   {t.name}: {(t.description or '').strip().splitlines()[0]}")
        print(f"      red flags: {', '.join(flags) or 'none'}  |  {status}")
        if "--pin" in sys.argv:
            pins[key] = fingerprint
    if "--pin" in sys.argv:
        PINS.write_text(json.dumps(pins, indent=2))
        print("   pinned.")


if "--files" in sys.argv:  # a well-known server, for comparison
    asyncio.run(audit("files", {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", str(HERE / "safety" / "office" / "public")]}))
else:
    version = ["--v2"] if "--v2" in sys.argv else []
    asyncio.run(audit("shipping", {"command": sys.executable, "args": [str(HERE / "sneaky_server.py"), *version]}))
