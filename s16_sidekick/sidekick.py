"""Sara's Sidekick: one create_agent worker with tools and middleware, plus an evaluator that checks the work."""
from datetime import date

from langchain.agents import create_agent
from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware, PIIMiddleware,
                                         TodoListMiddleware, wrap_tool_call)
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from pydantic import BaseModel, Field

from sidekick_tools import Browser, check_stock, notify_sara, place_reorder, read_file, web_search, write_file

PROMPT = """You are Sara's Sidekick, a coworker for Sara's Shop, a small handmade homeware shop.
Work until the task is done: plan with your to-do list, use your tools, and check your own work.

What you should know:
- Sara's prices: Lavender candle 12 euros, Candle trio 22 euros, Speckled mug 14 euros, Blue mug set 24 euros.
- Her competitor Wick & Co has a website at http://localhost:8015. Read pages with browser_snapshot (no arguments)
  and follow links with browser_click. Apply any sale before comparing prices.
- Save anything Sara asked you to write into the sandbox with write_file.
- Only contact Sara with notify_sara, and only place supplier orders with place_reorder. Both need her approval."""


class Evaluation(BaseModel):
    feedback: str = Field(description="What was good, and what is missing, in one or two sentences")
    success_criteria_met: bool = Field(description="True only if every success criterion is clearly met")


@wrap_tool_call
async def tolerate_tool_errors(request, handler):
    """If a tool fails, tell the model instead of crashing, so it can try another way."""
    try:
        return await handler(request)
    except Exception as error:
        return ToolMessage(content=f"Tool failed: {error}. Try another approach.", tool_call_id=request.tool_call["id"])


class Sidekick:
    async def setup(self):
        self.browser = Browser()
        self.tools = [check_stock, web_search, write_file, read_file, notify_sara, place_reorder] + await self.browser.start()
        self.worker = create_agent(
            model="openai:gpt-5.4-mini",
            tools=self.tools,
            system_prompt=f"{PROMPT}\n\nToday is {date.today():%A %d %B %Y}.",
            middleware=[
                tolerate_tool_errors,
                TodoListMiddleware(),
                PIIMiddleware("email", strategy="redact"),
                ModelCallLimitMiddleware(run_limit=30),
                HumanInTheLoopMiddleware(interrupt_on={"notify_sara": True, "place_reorder": True}),
            ],
            checkpointer=InMemorySaver(),
        )
        self.evaluator = ChatOpenAI(model="gpt-5.4-mini").with_structured_output(Evaluation)
        self.config = {"configurable": {"thread_id": "sidekick"}}

    async def start(self, task: str, criteria: str):
        """Begin a task. Returns ('approve', requests) if Sara must approve something, else ('done', reply, evaluation)."""
        self.task, self.criteria, self.tries = task, criteria, 1
        return await self._advance({"messages": [("user", f"{task}\n\nSuccess criteria: {criteria}")]})

    async def resume(self, approved: bool, note: str = ""):
        """Sara's decision, applied to every paused tool call."""
        decision = {"type": "approve"} if approved else {"type": "reject", "message": note or "Sara said no."}
        return await self._advance(Command(resume={"decisions": [decision] * len(self.waiting)}))

    async def _advance(self, payload):
        result = await self.worker.ainvoke(payload, self.config)
        if "__interrupt__" in result:
            self.waiting = result["__interrupt__"][0].value["action_requests"]
            return "approve", self.waiting
        reply = result["messages"][-1].content
        evaluation = await self.evaluate(reply)
        if not evaluation.success_criteria_met and self.tries < 3:
            self.tries += 1
            return await self._advance({"messages": [("user", f"Not done yet. Evaluator feedback: {evaluation.feedback}")]})
        return "done", reply, evaluation

    async def evaluate(self, reply: str) -> Evaluation:
        tools = [c["name"] for m in self.worker.get_state(self.config).values["messages"] for c in getattr(m, "tool_calls", None) or []]
        prompt = (f"You check whether an assistant met the success criteria for a task.\n"
                  f"Task: {self.task}\nSuccess criteria: {self.criteria}\n"
                  f"Tools it used: {', '.join(tools)}\nIts final reply: {reply}\n"
                  "Decide whether every success criterion was met.")
        return await self.evaluator.ainvoke(prompt)

    def todos(self) -> list[dict]:
        return self.worker.get_state(self.config).values.get("todos", [])

    async def close(self):
        await self.browser.close()
