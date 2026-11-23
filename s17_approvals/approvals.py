"""B8: the approval workflow as a LangGraph graph: read -> check rules -> approve / ask Sara / reject -> audit log."""
import json
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from pydantic import BaseModel, Field

import rules

load_dotenv(override=True)
AUDIT_LOG = Path(__file__).parent / "audit_log.jsonl"


class RequestForm(BaseModel):
    kind: Literal["refund", "expense"]
    who: str = Field(description="The customer or staff member asking")
    item: str = Field(description="What it is for, in a few words")
    order: Optional[str] = Field(description="The order number, if there is one")
    amount_eur: float = Field(description="The amount in euros")
    reason: Literal["damaged", "changed_mind", "wrong_item", "staff_purchase", "other"]
    has_photo: bool = Field(description="True if a photo or receipt is attached or shown")
    is_candle: bool = Field(description="True if the item is a candle")
    used: bool = Field(description="True if the item was used, lit or opened")
    days_since_delivery: Optional[int] = Field(description="Days since delivery, only if the message says")


reader = ChatOpenAI(model="gpt-5.4-mini").with_structured_output(RequestForm)


class State(TypedDict, total=False):
    text: str
    form: dict  # plain data, so checkpoints can save it
    path: str
    rule: str
    decision: str
    decided_by: str


def read_request(state: State) -> State:
    form = reader.invoke(f"Fill in the form for this refund or expense request. Do not decide anything.\n\n{state['text']}")
    return {"form": form.model_dump()}


def check_rules(state: State) -> State:
    path, rule = rules.check(RequestForm(**state["form"]))
    return {"path": path, "rule": rule}


def approve(state: State) -> State:
    return {"decision": "approved", "decided_by": "workflow"}


def reject(state: State) -> State:
    return {"decision": "rejected", "decided_by": "workflow"}


def ask_sara(state: State) -> State:
    f = RequestForm(**state["form"])
    answer = interrupt({"question": f"Approve {f.amount_eur:.2f} euros for {f.who}?", "item": f.item,
                        "order": f.order, "photo": f.has_photo, "rule": state["rule"]})
    return {"decision": "approved" if answer == "approve" else "rejected", "decided_by": "Sara"}


def write_log(state: State) -> State:
    f = RequestForm(**state["form"])
    entry = {"time": datetime.now().isoformat(timespec="seconds"), "who": f.who, "kind": f.kind, "item": f.item,
             "order": f.order, "amount_eur": f.amount_eur, "rule": state["rule"], "decision": state["decision"],
             "decided_by": state["decided_by"]}
    with open(AUDIT_LOG, "a") as log:
        log.write(json.dumps(entry) + "\n")
    return {}


def make_graph(checkpointer=None):
    builder = StateGraph(State)
    builder.add_node("read_request", read_request)
    builder.add_node("check_rules", check_rules)
    builder.add_node("approve", approve)
    builder.add_node("ask_sara", ask_sara)
    builder.add_node("reject", reject)
    builder.add_node("write_log", write_log)
    builder.add_edge(START, "read_request")
    builder.add_edge("read_request", "check_rules")
    builder.add_conditional_edges("check_rules", lambda s: s["path"], ["approve", "ask_sara", "reject"])
    for node in ("approve", "ask_sara", "reject"):
        builder.add_edge(node, "write_log")
    builder.add_edge("write_log", END)
    return builder.compile(checkpointer=checkpointer)
