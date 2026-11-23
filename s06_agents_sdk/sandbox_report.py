"""A sandbox agent: it gets its own workspace with Sara's sales file, runs commands there, and writes a report."""
import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import LocalFile
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient

load_dotenv()
DATA = Path(__file__).parent.parent / "data"

analyst = SandboxAgent(
    name="Sales analyst",
    instructions="You analyse sales files for Sara's shop. Calculate with shell tools like awk and sort; never guess numbers. When done, reply in one short sentence.",
    model="gpt-5.4-mini",
    default_manifest=Manifest(entries={
        "sales.csv": LocalFile(src=DATA / "october_sales.csv"),  # the only file the agent gets
    }),
)


async def main():
    client = UnixLocalSandboxClient()
    sandbox = await client.create(manifest=analyst.default_manifest)
    async with sandbox:
        result = await Runner.run(
            analyst,
            "Revenue is qty × price_eur. Write report.md with two small tables: the top 3 items by revenue, "
            "and revenue per weekday, best first. Then read report.md back and fix any mistake.",
            run_config=RunConfig(sandbox=SandboxRunConfig(session=sandbox)),
        )
        for item in result.new_items:  # what the agent did inside its workspace
            if item.type == "tool_call_item":
                command = json.loads(item.raw_item.arguments).get("cmd", "")
                print("ran:", command.splitlines()[0][:80])
        print(result.final_output)
        report = await sandbox.read(Path("report.md"))  # copy the report out before the workspace is removed
        (DATA / "october_report.md").write_bytes(report.read())
    print("\nSaved data/october_report.md")


asyncio.run(main())
