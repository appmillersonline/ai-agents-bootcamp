"""B11: split Sara's documents into sections and build a small search index with OpenAI embeddings."""
import json
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parents[1] / ".env", override=True)
HERE = Path(__file__).parent
client = OpenAI()

chunks = []
for doc in sorted((HERE / "docs").glob("*.md")):
    for part in re.split(r"\n(?=#{2,3} )", doc.read_text()):          # one chunk per ## or ### section
        lines = part.strip().splitlines()
        if len(lines) < 2:
            continue                                                   # skip bare titles
        chunks.append({"source": doc.name, "section": lines[0].lstrip("# "), "text": "\n".join(lines[1:]).strip()})

response = client.embeddings.create(model="text-embedding-3-small",
                                    input=[f"{c['section']}\n{c['text']}" for c in chunks])
for chunk, item in zip(chunks, response.data):
    chunk["vector"] = item.embedding

(HERE / "kb_index.json").write_text(json.dumps(chunks))
print(f"documents: {len(list((HERE / 'docs').glob('*.md')))}, chunks: {len(chunks)}, "
      f"tokens: {response.usage.total_tokens}, cost: about ${response.usage.total_tokens * 0.02 / 1e6:.5f}")
for c in chunks[:3]:
    print(f"  {c['source']} § {c['section']}: {c['text'][:60]}...")
