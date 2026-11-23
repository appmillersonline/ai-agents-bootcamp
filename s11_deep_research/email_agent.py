"""Agent 4: turns the report into an email and sends it to the test inbox."""
from agents import Agent, ModelSettings, function_tool

from inbox import send_email
from settings import MODEL


@function_tool
def send_email_tool(subject: str, body: str) -> str:
    """Send the research email to Sara.

    Args:
        subject: A short, clear subject line.
        body: The email text: a friendly opening, the summary, the next steps, then the report.
    """
    return send_email("sara@example.com", subject, body)


email_agent = Agent(
    name="Emailer",
    instructions="Turn the report into a plain-text email for Sara, keeping every section and number. "
                 "No markdown symbols. Sign it 'Your research team', then send it with your tool.",
    model=MODEL,
    tools=[send_email_tool],
    model_settings=ModelSettings(tool_choice="required"),
)
