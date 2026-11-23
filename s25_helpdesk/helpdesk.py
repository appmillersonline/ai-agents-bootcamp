"""Week 1: the IT helpdesk agent. Answers from the IT guide, checks the status page, opens tickets,
refuses passwords in chat, and needs a person to approve a password reset."""
import asyncio
import json
import re
import sys
from pathlib import Path

from agents import (Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, Runner, function_tool,
                    input_guardrail)
from dotenv import load_dotenv

load_dotenv(override=True)
HERE = Path(__file__).parent
TICKETS = HERE / "tickets.json"


@function_tool
def search_guide(topic: str) -> str:
    """Find the section of the IT guide about a topic, for example "printer" or "vpn"."""
    sections = re.split(r"\n(?=## )", (HERE / "it_guide.md").read_text())
    words = topic.lower().split()
    best = max(sections, key=lambda s: sum(s.lower().count(w) for w in words))
    return best.strip()


@function_tool
def check_status(service: str) -> str:
    """Check the live status of a service: email, vpn, printer or shop website."""
    status = json.loads((HERE / "status.json").read_text())
    return f"{service}: {status.get(service.lower(), 'unknown service')}"


@function_tool
def create_ticket(summary: str, priority: str) -> str:
    """Open a ticket for a person in IT. priority is low, normal or high."""
    tickets = json.loads(TICKETS.read_text()) if TICKETS.exists() else []
    tickets.append({"id": len(tickets) + 1, "summary": summary, "priority": priority})
    TICKETS.write_text(json.dumps(tickets, indent=2))
    return f"Ticket {len(tickets)} opened ({priority})."


@function_tool(needs_approval=True)                 # a person must approve every call
def reset_password(username: str) -> str:
    """Reset a user's password and send them a one-time link. Only after the self-service page failed."""
    return f"Password reset for {username}; a one-time link was sent to their phone."


PASSWORD_PATTERN = re.compile(            # "password is X", "it's X" after "password", "pw: X"...
    r"\b(pass(word)?|pw|pin)\b[^.!]{0,40}?\b(is|it's|it is|=|:)\s*['\"]?(?=\S*[\d!@#$%])\S{6,}", re.I)


@input_guardrail(run_in_parallel=False)          # check first; the model never sees a blocked message
async def no_passwords(ctx, agent, message) -> GuardrailFunctionOutput:
    """Stop the run if someone pastes what looks like a password."""
    looks_like = bool(PASSWORD_PATTERN.search(str(message)))
    return GuardrailFunctionOutput(output_info={"password_seen": looks_like}, tripwire_triggered=looks_like)


agent = Agent(
    name="helpdesk", model="gpt-5.4-mini",
    instructions="You are the IT helpdesk for Sara's small shop. Search the IT guide before answering, and check the "
                 "status page for service problems. Give short, step-by-step answers. Open a ticket when the guide "
                 "doesn't solve it. Only use reset_password after the user says the self-service page failed.",
    tools=[search_guide, check_status, create_ticket, reset_password],
    input_guardrails=[no_passwords],
)


async def ask(question: str, approve: bool | None = None):
    print(f"user: {question}")
    try:
        result = await Runner.run(agent, question)
    except InputGuardrailTripwireTriggered:
        print("  [guardrail] message stopped: it looks like it contains a password")
        return
    while result.interruptions:                    # the run paused: a tool needs a person's yes
        state = result.to_state()
        for item in result.interruptions:
            print(f"  [approval needed] {item.raw_item.name}({item.raw_item.arguments}) -> {'approved' if approve else 'rejected'}")
            state.approve(item) if approve else state.reject(item)
        result = await Runner.run(agent, state)
    for item in result.new_items:
        if item.type == "tool_call_item":
            print(f"  [{item.raw_item.name}] {item.raw_item.arguments}")
    print(f"helpdesk: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(ask(sys.argv[1], approve={"yes": True, "no": False}.get(sys.argv[2]) if len(sys.argv) > 2 else None))
