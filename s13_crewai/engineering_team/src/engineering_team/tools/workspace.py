from pathlib import Path

from crewai.tools import tool

WORKSPACE = Path(__file__).parents[3] / "sara_app"
WORKSPACE.mkdir(exist_ok=True)


@tool("List workspace files")
def list_files() -> str:
    """List the files in the sara_app folder, the only folder the team can use."""
    names = sorted(p.name for p in WORKSPACE.iterdir())
    return "\n".join(names) or "The workspace is empty."


@tool("Read a workspace file")
def read_file(filename: str) -> str:
    """Read one file from the sara_app folder."""
    return (WORKSPACE / Path(filename).name).read_text()


@tool("Write a workspace file")
def write_file(filename: str, content: str) -> str:
    """Write a file in the sara_app folder. An existing file is replaced."""
    (WORKSPACE / Path(filename).name).write_text(content)
    return f"Wrote {filename}"


workspace_tools = [list_files, read_file, write_file]
