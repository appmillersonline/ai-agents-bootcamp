from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from shop import tools_used

SANDBOX = Path(__file__).parent / "sandbox"

stall_planner = {
    "name": "stall-planner",
    "description": "Turns a market recommendation into a one-page stall plan for Sara.",
    "system_prompt": "You turn market research into practical plans for Sara's Shop. Save the plan to the file you are asked for.",
    "skills": ["/skills/"],
}

lead = create_deep_agent(
    model="openai:gpt-5.4-mini",
    system_prompt="You help Sara's Shop prepare for markets. The stall planner writes plans itself; never rewrite its file.",
    subagents=[stall_planner],
    backend=FilesystemBackend(root_dir=SANDBOX, virtual_mode=True),
)

result = lead.invoke({"messages": [("user", "Read compare.md and ask the stall planner to write a stall plan for the recommended market to stall_plan.md.")]})
print("Tools used:", " -> ".join(tools_used(result)))
print("\n" + result["messages"][-1].text)
