"""The pptx skill: Claude builds a real PowerPoint deck from Sara's sales."""
import zipfile
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
DATA = Path(__file__).parent.parent / "data"

uploaded = client.files.upload(file=DATA / "october_sales.csv")
response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    betas=["code-execution-2025-08-25"],
    container={"skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]},
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Make october_review.pptx with 3 slides: the October total, the top 3 items, "
                                 "and the best weekday. Big numbers, few words. Reply in one sentence."},
        {"type": "container_upload", "file_id": uploaded.id},
    ]}],
)
for block in response.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "bash_code_execution_tool_result":
        for item in getattr(block.content, "content", None) or []:
            if item.type == "bash_code_execution_output":
                name = client.files.retrieve_metadata(item.file_id).filename
                client.files.download(item.file_id).write_to_file(DATA / name)
                slides = [n for n in zipfile.ZipFile(DATA / name).namelist() if n.startswith("ppt/slides/slide")]
                print(f"Saved: data/{name} with {len(slides)} slides")
client.files.delete(uploaded.id)
