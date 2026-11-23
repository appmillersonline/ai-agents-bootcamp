"""Agentic RAG through MCP: the Qdrant server stores Sara's handbook by meaning, all on this laptop."""
import asyncio
import re
from pathlib import Path

from agents.mcp import MCPServerStdio

HERE = Path(__file__).parent
QDRANT = {"command": "uvx", "args": ["--python", "3.12", "mcp-server-qdrant"],  # 3.12: its pinned packages have no build for 3.14 yet
          "env": {"QDRANT_LOCAL_PATH": str(HERE / "memory" / "qdrant"), "COLLECTION_NAME": "handbook"}}


def handbook_rules() -> list[str]:
    """Split Sara's handbook into short rules, one bullet point each."""
    text = (HERE.parent / "data" / "shop_handbook.md").read_text()
    return [re.sub(r"^- ", "", line).strip() for line in text.splitlines() if line.startswith("- ")]


async def main():
    async with MCPServerStdio(params=QDRANT, name="qdrant", client_session_timeout_seconds=180) as qdrant:
        print("tools:", ", ".join(t.name for t in await qdrant.list_tools()))
        rules = handbook_rules()
        for rule in rules:
            await qdrant.call_tool("qdrant-store", {"information": rule})
        print(f"stored {len(rules)} handbook rules as vectors")


if __name__ == "__main__":
    asyncio.run(main())
