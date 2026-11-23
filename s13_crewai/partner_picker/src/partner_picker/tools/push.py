import os

import requests
from crewai.tools import tool


@tool("Send a push notification")
def send_push(message: str) -> str:
    """Send a short push notification to Sara's phone. Use it once, for the final decision."""
    try:
        requests.post(f"https://ntfy.sh/{os.environ['NTFY_TOPIC']}", data=message.encode(), timeout=10).raise_for_status()
    except requests.RequestException as e:
        return f"Push notification FAILED: {e}. Tell Sara it was not sent."
    return "Push notification sent"
