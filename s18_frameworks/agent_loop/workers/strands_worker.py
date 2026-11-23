"""Strands worker: same three tools, Strands spelling."""
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.openai import OpenAIModel

from agent_loop.worker_tools import WORKER_PROMPT, make_tools

load_dotenv(override=True)
read_task, save_file, complete_task = (tool(f) for f in make_tools("strands"))
agent = Agent(model=OpenAIModel(model_id="gpt-5.4-mini"), system_prompt=WORKER_PROMPT,
              tools=[read_task, save_file, complete_task], callback_handler=None)
agent("Do your task on the board.")
