"""Search by meaning, no model: three customer phrasings, the two closest handbook rules for each."""
import asyncio
import json
import re

from agents.mcp import MCPServerStdio

from rag_store import QDRANT

QUERIES = ["where is my package", "the parcel came smashed", "my mug arrived in pieces"]


async def main():
    async with MCPServerStdio(params=QDRANT, name="handbook", client_session_timeout_seconds=120) as handbook:
        for query in QUERIES:
            result = await handbook.call_tool("qdrant-find", {"query": query})
            entries = json.loads(result.content[0].text)[1:]   # item 0 is a header; then the closest rules, best first
            print(f"{query!r}")
            for entry in entries[:2]:
                print("   ->", re.sub(r"</?entry>|</?content>|<metadata>.*?</metadata>", "", entry).strip()[:100])


asyncio.run(main())
