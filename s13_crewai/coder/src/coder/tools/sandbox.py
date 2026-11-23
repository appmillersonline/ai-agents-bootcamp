import subprocess
from pathlib import Path

from crewai.tools import tool

SANDBOX = Path(__file__).parents[3] / "sandbox"
SANDBOX.mkdir(exist_ok=True)


@tool("List sandbox files")
def list_files() -> str:
    """List the files in the sandbox folder, the only folder you can use."""
    names = sorted(p.name for p in SANDBOX.iterdir())
    return "\n".join(names) or "The sandbox is empty."


@tool("Read a sandbox file")
def read_file(filename: str) -> str:
    """Read one file from the sandbox folder."""
    return (SANDBOX / Path(filename).name).read_text()


@tool("Write a sandbox file")
def write_file(filename: str, content: str) -> str:
    """Write a file in the sandbox folder. An existing file is replaced."""
    (SANDBOX / Path(filename).name).write_text(content)
    return f"Wrote {filename}"


@tool("Run a Python file in Docker")
def run_python(filename: str) -> str:
    """Run a Python file from the sandbox inside a fresh Docker container, with no network,
    and return what it printed. The container is deleted afterwards."""
    cmd = ["docker", "run", "--rm", "--network", "none", "-v", f"{SANDBOX}:/work", "-w", "/work",
           "python:3.13-slim", "python", Path(filename).name]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.stdout + result.stderr


sandbox_tools = [list_files, read_file, write_file, run_python]
