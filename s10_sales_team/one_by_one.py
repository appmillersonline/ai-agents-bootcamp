"""The same three writers, one after another, to see what asyncio.gather saves."""
import asyncio
import time

from dotenv import load_dotenv
from agents import Runner

from sales_kit import WRITERS

load_dotenv()
TASK = "Write to Lena, owner of Café Lumen, a busy coffee shop."


async def main():
    start = time.time()
    for writer in WRITERS:
        result = await Runner.run(writer, TASK)
        print(f"{writer.name}: done after {time.time() - start:.1f} s")
    print(f"\nOne by one: {time.time() - start:.1f} s")

    start = time.time()
    await asyncio.gather(*(Runner.run(w, TASK) for w in WRITERS))
    print(f"All at once: {time.time() - start:.1f} s")


asyncio.run(main())
