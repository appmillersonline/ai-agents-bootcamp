"""Project 10: the AI Trading Floor. A researcher and three traders, each with their own style. Simulated money only."""
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from agents import Agent, Runner, set_trace_processors
from agents.mcp import MCPServerStdio
from agents.tracing.processor_interface import TracingProcessor
from dotenv import load_dotenv


load_dotenv(override=True)
HERE = Path(__file__).parent
MODEL = "gpt-5.4-mini"

TRADERS = {
    "Mia": "You follow momentum: buy companies whose price has been rising, sell ones that are falling.",
    "Vic": "You are a value trader: you like companies that have fallen but have solid news, and you avoid hype.",
    "Cora": "You are careful: you keep at least half your money in cash and spread the rest over several companies.",
}


class LocalTraces(TracingProcessor):
    """Keep every trace on this computer, in traces.jsonl, instead of sending it anywhere."""
    def on_trace_start(self, trace): pass
    def on_trace_end(self, trace): pass
    def on_span_start(self, span): pass
    def on_span_end(self, span):
        with open(HERE / "traces.jsonl", "a") as f:
            f.write(json.dumps({"trace": span.trace_id, "type": span.span_data.type,
                                "data": span.span_data.export(), "ms": _ms(span)}, default=str) + "\n")
    def shutdown(self): pass
    def force_flush(self): pass


def _ms(span):
    try:
        from datetime import datetime
        return int((datetime.fromisoformat(span.ended_at) - datetime.fromisoformat(span.started_at)).total_seconds() * 1000)
    except Exception:
        return None


def server(name, script):
    return MCPServerStdio(name=name, client_session_timeout_seconds=30,
                          params={"command": sys.executable, "args": [str(HERE / script)],
                                  "env": {**os.environ}})          # MCP servers only get a few variables unless you pass them


async def trade_one(name, style, market, accts):
    researcher = Agent(name="researcher", model=MODEL, mcp_servers=[market],
                       instructions="You research the simulated market. Use the tools, then give a short brief: "
                                    "price trend and news for the companies asked about. Facts only, no advice.")
    trader = Agent(
        name=name, model=MODEL, mcp_servers=[accts],
        tools=[researcher.as_tool(tool_name="ask_researcher", tool_description="Ask the researcher about companies on the market.")],
        instructions=f"You are {name}, a trader on a simulated market with fake money. {style}\n"
                     f"Check your portfolio, ask the researcher, then make at most three trades, each with a one-sentence reason. "
                     f"Always pass trader='{name}'. Finish with one sentence about what you did.")
    result = await Runner.run(trader, "Today's trading session is open.", max_turns=15)
    return name, result


async def main():
    set_trace_processors([LocalTraces()])                 # traces stay local
    import accounts                                       # after MARKET_DAY is set
    for name in TRADERS:
        accounts.open_account(name)
    start = time.time()
    async with server("market", "market_server.py") as market, server("accounts", "accounts_server.py") as accts:
        results = await asyncio.gather(*(trade_one(n, s, market, accts) for n, s in TRADERS.items()))
    for name, result in results:
        print(f"== {name}")
        for item in result.new_items:
            if item.type == "tool_call_item" and item.raw_item.name in ("buy_shares", "sell_shares"):
                a = json.loads(item.raw_item.arguments)
                print(f"  {item.raw_item.name.split('_')[0]} {a['shares']} {a['ticker']}: {a['reason']}")
            elif item.type == "tool_call_output_item" and "Rejected" in str(item.output):
                print(f"     {str(item.output).split('Rejected')[1].split(chr(39))[0].strip(': ')[:100]}  (rejected)")
        print(f"  {name}: {result.final_output}")
    for name in TRADERS:
        accounts.snapshot(name)
    print(f"== day {accounts.TODAY} done in {time.time() - start:.0f} s")


if __name__ == "__main__":
    os.environ["MARKET_DAY"] = sys.argv[1] if len(sys.argv) > 1 else "30"
    asyncio.run(main())
