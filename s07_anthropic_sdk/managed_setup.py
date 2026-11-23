"""Managed Agents, step 1 (run once): create the environment and the agent, and save their ids."""
import json
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
IDS = Path(__file__).parent.parent / "data" / "managed_ids.json"

environment = client.beta.environments.create(  # the kind of workspace each session gets
    name="saras-shop-env",
    config={"type": "cloud", "networking": {"type": "limited"}},
)

agent = client.beta.agents.create(  # the agent: model, instructions and tools, saved by Anthropic
    name="Sara's sales analyst",
    model="claude-opus-5-5",
    system="You analyse sales files for Sara's shop. Use code to calculate; never guess numbers.",
    tools=[{
        "type": "agent_toolset_20260401",  # bash, files and code in its own workspace
        "default_config": {"enabled": True, "permission_policy": {"type": "auto"}},
        "configs": [{"name": "web_fetch", "enabled": False}, {"name": "web_search", "enabled": False}],
    }],
)

IDS.write_text(json.dumps({"environment": environment.id, "agent": agent.id, "version": agent.version}, indent=1))
print("Environment:", environment.id)
print("Agent:", agent.id, "version", agent.version)
