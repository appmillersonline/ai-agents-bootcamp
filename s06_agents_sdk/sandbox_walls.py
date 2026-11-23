"""Check the sandbox walls yourself: run a few commands inside a workspace, no model needed."""
import asyncio
from pathlib import Path

from agents.sandbox import Manifest
from agents.sandbox.entries import LocalFile
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient

DATA = Path(__file__).parent.parent / "data"
TESTS = ["ls", "ls ..", "touch ../note.txt"]


async def main():
    manifest = Manifest(entries={"sales.csv": LocalFile(src=DATA / "october_sales.csv")})
    sandbox = await UnixLocalSandboxClient().create(manifest=manifest)
    async with sandbox:
        for command in TESTS:
            result = await sandbox.exec(command, shell=True)
            answer = (result.stdout or result.stderr).decode().strip().split(": ")[-1]
            print(f"{command:<18} -> {answer}")


asyncio.run(main())
