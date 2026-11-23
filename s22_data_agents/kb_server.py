"""B11: Sara's company knowledge as an MCP server: search the documents, get sections with their sources."""
import json
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from openai import OpenAI

HERE = Path(__file__).parent
load_dotenv(HERE.parent / ".env", override=True)
client = OpenAI()
chunks = json.loads((HERE / "kb_index.json").read_text())
vectors = np.array([c["vector"] for c in chunks])
vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
mcp = FastMCP("sara-knowledge", log_level="WARNING")


@mcp.tool()
def search_docs(query: str, k: int = 3) -> str:
    """Search Sara's company documents (customer handbook, staff guide, supplier guide).
    Returns the best matching sections, each with its source file, section title and a match score from 0 to 1.

    Args:
        query: What to look for, in plain words, for example "holiday rules".
        k: How many sections to return.
    """
    q = np.array(client.embeddings.create(model="text-embedding-3-small", input=query).data[0].embedding)
    scores = vectors @ (q / np.linalg.norm(q))
    best = np.argsort(scores)[::-1][:k]
    return "\n\n".join(f"[{chunks[i]['source']} § {chunks[i]['section']}] (score {scores[i]:.2f})\n{chunks[i]['text']}"
                       for i in best)


if __name__ == "__main__":
    mcp.run()
