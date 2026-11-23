"""Memory: a session keeps the conversation, so the agent remembers what you said earlier."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession

load_dotenv()

agent = Agent(name="Shop assistant", instructions="You help customers of Sara's shop. Be short.", model="gpt-5.4-mini")


async def main():
    # Without a session, every run starts from a blank page
    await Runner.run(agent, "Hi, I'm Tom and I'm looking for a vase.")
    result = await Runner.run(agent, "What's my name, and what am I looking for?")
    print("No session:  ", result.final_output)

    # With a session, the SDK saves every message and sends them again next time
    session = SQLiteSession("tom-chat", "memory.db")
    await Runner.run(agent, "Hi, I'm Tom and I'm looking for a vase.", session=session)
    result = await Runner.run(agent, "What's my name, and what am I looking for?", session=session)
    print("With session:", result.final_output)


asyncio.run(main())
