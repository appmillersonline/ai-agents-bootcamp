"""B9: sort, summarise and prioritise Sara's inbox with structured output (the model reads; it never sends)."""
import json
from typing import Literal

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv(override=True)


class Triage(BaseModel):
    category: Literal["order_question", "refund", "wholesale", "supplier", "complaint", "praise", "spam", "phishing", "newsletter"]
    urgency: Literal["today", "this_week", "no_rush"]
    summary: str = Field(description="One short sentence: who wants what")
    needs_reply: bool = Field(description="True if Sara or the shop should answer this email")


sorter = ChatOpenAI(model="gpt-5.4-mini").with_structured_output(Triage)
PROMPT = ("You sort emails for Sara's Shop, a small handmade homeware shop. Phishing (asks for passwords or logins) "
          "and spam never need a reply. Today means: a customer is upset or waiting, or money is at stake soon.\n\n")


def load_inbox(path="inbox_monday.json"):
    return json.load(open(path))


def triage_all(emails):
    prompts = [PROMPT + f"From: {e['from']}\nSubject: {e['subject']}\n\n{e['body']}" for e in emails]
    return sorter.batch(prompts)  # all emails at once, in parallel
