"""Managed Agents keeps a record: list your recent sessions, their status and what they used."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

for session in list(client.beta.sessions.list())[:5]:  # the newest sessions first
    used = session.usage
    print(f"{session.created_at:%d %b %H:%M}  {session.status:<6} {used.active_seconds:>5.0f} s of work, "
          f"{used.output_tokens:>5} tokens written, {used.cache_read_input_tokens:>6} read from cache")
