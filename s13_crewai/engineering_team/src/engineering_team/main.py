from engineering_team.crew import EngineeringTeam

REQUIREMENTS = """
A gift card system for Sara's candle shop.
- Sara can issue a gift card with a starting balance in euros. Each card gets a short code like SARA-1234.
- A customer can spend from a card. A purchase bigger than the balance is refused, and nothing is taken.
- Sara can check a card's balance and see its history: issued, spent and refused, with amounts.
- Sara can cancel a card. A cancelled card can't be spent.
- Every amount must be more than zero.
"""


def run():
    EngineeringTeam().crew().kickoff(inputs={
        "requirements": REQUIREMENTS,
        "module_name": "giftcards.py",
        "class_name": "GiftCards",
    })
