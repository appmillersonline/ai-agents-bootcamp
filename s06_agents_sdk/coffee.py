"""Async Python with a coffee shop: one barista, three orders. Waiting in a line vs. waiting together."""
import asyncio
import time


async def make_coffee(name, seconds):
    print(f"Start {name}")
    await asyncio.sleep(seconds)  # the machine is busy; the barista is free to start another order
    print(f"Done  {name}")
    return name


async def one_by_one():
    for name in ["latte", "espresso", "tea"]:
        await make_coffee(name, 2)


async def all_together():
    await asyncio.gather(make_coffee("latte", 2), make_coffee("espresso", 2), make_coffee("tea", 2))


start = time.time()
asyncio.run(one_by_one())
print(f"One by one: {time.time() - start:.1f} s\n")

start = time.time()
asyncio.run(all_together())
print(f"All together: {time.time() - start:.1f} s")
