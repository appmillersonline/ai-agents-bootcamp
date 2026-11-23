"""Code execution: Claude writes and runs Python on Anthropic's servers, on your file."""
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
SALES = Path(__file__).parent.parent / "data" / "october_sales.csv"

uploaded = client.files.upload(file=SALES)  # send the file once, get an id back

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=8000,
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Which item earned the most in October (qty × price_eur), and on which weekday "
                                 "did the shop earn the most? Use Python. Answer in two short lines."},
        {"type": "container_upload", "file_id": uploaded.id},  # the file appears in Claude's workspace
    ]}],
)

for block in response.content:
    if block.type == "server_tool_use":
        print("Claude runs:", block.input.get("command", block.input.get("code", ""))[:80].replace("\n", " "))
    elif block.type == "text":
        print(block.text)

client.files.delete(uploaded.id)  # tidy up the uploaded file
