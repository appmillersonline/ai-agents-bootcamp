"""Test Sara's server with no model at all: call each tool directly and check the answers."""
import asyncio
import sys
from pathlib import Path

from agents.mcp import MCPServerStdio

SERVER = {"command": sys.executable, "args": [str(Path(__file__).parent / "shop_server.py")]}
CHECKS = [  # (tool, arguments, text the answer must contain)
    ("check_stock", {"item": "Candle trio"}, "0 in stock"),
    ("check_stock", {"item": "candle trio"}, "0 in stock"),      # any capital letters
    ("check_stock", {"item": "Teapot"}, "not a product"),          # an item Sara doesn't sell
    ("find_order", {"order_id": "#1042"}, "shipped"),              # with a hash sign
    ("low_stock", {}, "Blue mug set, Candle trio"),
]


async def main():
    async with MCPServerStdio(params=SERVER, name="sara-shop", client_session_timeout_seconds=30) as shop:
        passed = 0
        for tool, args, expected in CHECKS:
            text = (await shop.call_tool(tool, args)).content[0].text
            ok = expected in text
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'}  {tool}({args}) -> {text}")
        print(f"\n{passed}/{len(CHECKS)} checks passed")
        resources = await shop.session.list_resources()
        page = await shop.session.read_resource("shop://handbook")
        print(f"resource: {resources.resources[0].uri} -> {page.contents[0].text.splitlines()[0]}")


asyncio.run(main())
