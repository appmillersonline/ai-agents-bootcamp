"""Agno with a SQLite database: the agent remembers what Sara told it, even after a restart."""
import sys
from pathlib import Path

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[2] / ".env", override=True)

agent = Agent(
    model=OpenAIChat(id="gpt-5.4-mini"),
    instructions="You are Sara's shop assistant. Be brief.",
    db=SqliteDb(db_file=str(Path(__file__).parent / "agno_memory.db")),  # saved on disk
    session_id="sara-shop-notes",   # same id = same conversation, every time
    add_history_to_context=True,    # send earlier messages to the model
)

response = agent.run(sys.argv[1])
print(f"Sara: {sys.argv[1]}")
print(f"agent: {response.content}")
