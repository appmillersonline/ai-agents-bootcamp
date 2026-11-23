"""Test the password guardrail's pattern on its own: no model, no cost."""
from helpdesk import PASSWORD_PATTERN

MESSAGES = {
    "Can you reset my password? It's Candle2024": True,
    "my password is Shop!2025, please check it": True,
    "pw: hunter22": True,
    "I forgot my password and the reset page failed.": False,
    "What's the wifi password? It's not on the card.": False,
    "The printer won't print.": False,
}
for text, should_block in MESSAGES.items():
    blocked = bool(PASSWORD_PATTERN.search(text))
    print(f"{'PASS' if blocked == should_block else 'FAIL'}  {'blocked' if blocked else 'allowed'}  {text}")
