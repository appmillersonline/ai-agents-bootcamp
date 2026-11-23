"""The three tools every Python worker gets. Each framework wraps them its own way."""
from agent_loop import board

WORKER_PROMPT = ("You are a worker on Sara's launch team. First call read_task to get your job and the launch brief. "
                 "Write the piece, then call save_file with the exact file name from the task. "
                 "Finally call complete_task. Use only facts from the brief. "
                 "If the task has a note, it says what to fix: follow it exactly. "
                 "Respect any word limit in the title; save_file tells you the word count, so check it and save again if needed.")


def make_tools(owner: str):
    def read_task() -> dict:
        """Get your current task from the shared board, plus the launch brief."""
        t = board.task_for(owner)
        if t is None:
            return {"error": "No task for you."}
        board.set_status(t["id"], "working")
        return {"task_id": t["id"], "title": t["title"], "file": t["file"], "note": t["note"],
                "brief": board.BRIEF.read_text()}

    def save_file(file: str, content: str) -> str:
        """Save your finished piece into the shared outbox folder.

        Args:
            file: The file name from your task, for example "product.md".
            content: The full text of the piece, in Markdown.
        """
        (board.OUTBOX / file).write_text(content)
        return f"Saved {file} ({len(content.split())} words)."

    def complete_task(task_id: int) -> str:
        """Mark your task as done on the shared board.

        Args:
            task_id: The task_id you got from read_task.
        """
        board.set_status(task_id, "done")
        return "Marked done."

    return read_task, save_file, complete_task
