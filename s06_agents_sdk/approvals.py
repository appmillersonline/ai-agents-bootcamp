"""Human in the loop: the agent may refund small amounts, but anything bigger waits for Sara's yes."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


async def over_20(ctx, params, call_id) -> bool:
    return params["amount"] > 20  # True means: pause and ask a person first


@function_tool(needs_approval=over_20)
def issue_refund(order_id: str, amount: int, reason: str) -> str:
    """Refund money to the customer for an order.

    Args:
        order_id: The order number, like 1042.
        amount: The refund in whole euros.
        reason: A short reason for the refund.
    """
    return f"Refunded €{amount} for order {order_id}."


support = Agent(
    name="Support",
    instructions="You help customers of Sara's shop. Refund what the customer says they paid. Reply in one sentence.",
    model="gpt-5.4-mini",
    tools=[issue_refund],
)


async def ask(message):
    print(f"Customer: {message}")
    result = await Runner.run(support, message)
    while result.interruptions:  # the run paused: a tool call needs a person
        state = result.to_state()
        for item in result.interruptions:
            answer = input(f"  Sara, approve {item.name} {item.arguments}? (y/n) ")
            if answer == "y":
                state.approve(item)
            else:
                state.reject(item, rejection_message="Sara said no. Offer store credit instead.")
        result = await Runner.run(support, state)  # carry on from where it stopped
    print(f"Agent: {result.final_output}\n")


async def main():
    await ask("Order 1041 came two days late, I paid €8 for shipping. Can I get that back?")
    await ask("The vase from order 1042 arrived cracked. I paid €45 for it. Please refund me.")


asyncio.run(main())
