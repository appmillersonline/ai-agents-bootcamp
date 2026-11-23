"""A framework decision chart, as plain code. No model needed: the questions come in a fixed order.

  uv run python choose.py --language python --cloud none --typed yes
"""
import argparse

ask = argparse.ArgumentParser(description="Which agent framework fits your project?")
ask.add_argument("--one-call", choices=["yes", "no"], default="no", help="Could one model call (or a fixed workflow) do the job?")
ask.add_argument("--language", choices=["python", "typescript", "dotnet"], default="python")
ask.add_argument("--cloud", choices=["none", "google", "aws", "azure"], default="none")
ask.add_argument("--typed", choices=["yes", "no"], default="no", help="Do the answers feed other code?")
ask.add_argument("--memory", choices=["yes", "no"], default="no", help="Must it remember things between runs?")
ask.add_argument("--branches", choices=["yes", "no"], default="no", help="Many steps, branches, approvals?")
a = ask.parse_args()


def choose(a) -> tuple[str, str, str]:
    """Return (pick, reason, runner-up). The order of the questions is the chart."""
    if a.one_call == "yes":
        return "No framework", "one model call or a plain Python workflow is simpler and easier to test", "OpenAI Agents SDK"
    if a.language == "typescript":
        return "Mastra", "TypeScript first, so the agent lives next to your web code", "OpenAI Agents SDK (JS)"
    if a.language == "dotnet" or a.cloud == "azure":
        return "Microsoft Agent Framework", "Python and .NET, and it fits the Microsoft stack", "OpenAI Agents SDK"
    if a.cloud == "google":
        return "Google ADK", "Gemini and Google Cloud, plus ADK Web and A2A built in", "OpenAI Agents SDK"
    if a.cloud == "aws":
        return "Strands Agents", "Bedrock by default and very little setup", "OpenAI Agents SDK"
    if a.branches == "yes":
        return "LangGraph", "a graph with checkpoints and human approvals", "Microsoft Agent Framework"
    if a.typed == "yes":
        return "Pydantic AI", "typed answers checked by Pydantic, ready for your code", "OpenAI Agents SDK + output_type"
    if a.memory == "yes":
        return "Agno", "storage and memory built in", "OpenAI Agents SDK + sessions"
    return "OpenAI Agents SDK", "small, clear, and the one you already know", "Google ADK"


pick, why, runner_up = choose(a)
print(f"Pick:      {pick}")
print(f"Why:       {why}")
print(f"Runner-up: {runner_up}")
