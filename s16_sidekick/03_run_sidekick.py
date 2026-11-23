import asyncio

from sidekick import Sidekick

TASK = ("Compare Wick & Co's candle prices with ours, check our stock of the Candle trio, "
        "write a short price check to price_check.md, and send me a one-line note with your verdict.")
CRITERIA = "price_check.md compares both candles with any sale applied, and states how many Candle trios we have."


def show_plan(sidekick):
    for todo in sidekick.todos():
        mark = {"completed": "x", "in_progress": ">"}.get(todo["status"], " ")
        print(f"  [{mark}] {todo['content']}")


async def main():
    sidekick = Sidekick()
    await sidekick.setup()
    print(f"Sidekick ready with {len(sidekick.tools)} tools.\n")
    outcome = await sidekick.start(TASK, CRITERIA)
    while outcome[0] == "approve":
        print("Plan so far:"); show_plan(sidekick)
        for request in outcome[1]:
            print(f"\nSara, approve {request['name']}? {request['args']}")
        answer = input("Approve? (y/n): ").strip().lower()
        outcome = await sidekick.resume(answer.startswith("y"))
    _, reply, evaluation = outcome
    print("\nPlan:"); show_plan(sidekick)
    print("\nSidekick:", reply)
    print(f"\nEvaluator: met={evaluation.success_criteria_met}. {evaluation.feedback}")
    await sidekick.close()


asyncio.run(main())
