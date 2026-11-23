"""Agent Skills: Anthropic's ready-made xlsx skill turns Sara's sales into a real Excel file."""
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
    container={"skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]},  # load the xlsx skill
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],  # skills run inside code execution
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Make an Excel file october_report.xlsx: one sheet with revenue per item "
                                 "(qty × price_eur), best first, and a bar chart. Reply in one sentence."},
        {"type": "container_upload", "file_id": uploaded.id},
    ]}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "bash_code_execution_tool_result":
        for item in getattr(block.content, "content", None) or []:  # files Claude created
            if item.type == "bash_code_execution_output":
                name = client.files.retrieve_metadata(item.file_id).filename
                client.files.download(item.file_id).write_to_file(DATA / name)
                print("Saved:", f"data/{name}")

client.files.delete(uploaded.id)
