"""Business Lab 2: a booking agent for Studio Nora, a small hair salon. It finds free slots, books, reschedules and cancels."""
import json
from datetime import date, datetime
from pathlib import Path

import gradio as gr

from agent import notify, run_agent, tool_json

HERE = Path(__file__).parent
BOOKINGS = HERE / "bookings.json"
OUTBOX = HERE.parent / "outbox"
OPEN_DAYS = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
SERVICES = {"Haircut": "€35", "Colour": "€80", "Beard trim": "€15"}


def load():
    return json.loads(BOOKINGS.read_text())


def save(bookings):
    BOOKINGS.write_text(json.dumps(bookings, indent=2))


def free_slots(day):
    """List the free times on one day, or say why that day doesn't work."""
    when = datetime.strptime(day, "%Y-%m-%d").date()
    if when < date.today():
        return {"error": "That day is in the past."}
    if when.strftime("%A") not in OPEN_DAYS:
        return {"error": f"We're closed on {when.strftime('%A')}s."}
    taken = [b["time"] for b in load() if b["day"] == day and b["status"] == "booked"]
    return {"day": day, "free": [t for t in HOURS if t not in taken]}


def confirm(booking, what):
    """Write a confirmation email to the outbox (nothing is sent), and tell Nora on her phone."""
    b = booking
    text = f"To: {b['email']}\nHi {b['name']}, your {b['service']} is {what}: {b['day']} at {b['time']}.\nThank you, Studio Nora"
    (OUTBOX / f"booking_{b['id']}.txt").write_text(text, encoding="utf-8")
    notify(f"{b['id']} {what}: {b['name']}, {b['service']}, {b['day']} {b['time']}")


def book(name, email, service, day, time):
    """Book a free slot, save it, and confirm it."""
    if time not in free_slots(day).get("free", []):
        return {"error": "That time isn't free. Check free_slots again."}
    bookings = load()
    booking = {"id": f"B{101 + len(bookings)}", "name": name, "email": email,
               "service": service, "day": day, "time": time, "status": "booked"}
    save(bookings + [booking])
    confirm(booking, "booked")
    return {"booked": booking}


def find(bookings, booking_id, email):
    """The customer's booking, only if the number and the email both match."""
    for b in bookings:
        if b["id"] == booking_id.upper() and b["email"].lower() == email.lower() and b["status"] == "booked":
            return b


def late_fee(b):
    """Our code does the date maths, not the model: €10 if the appointment is less than 24 hours away."""
    start = datetime.strptime(f"{b['day']} {b['time']}", "%Y-%m-%d %H:%M")
    return "€10" if (start - datetime.now()).total_seconds() < 24 * 3600 else "none"


def my_bookings(email):
    """List a customer's upcoming bookings, each with the late fee if they cancel now."""
    mine = [b | {"late_fee": late_fee(b)} for b in load() if b["email"].lower() == email.lower() and b["status"] == "booked"]
    return {"bookings": mine} if mine else {"error": "No bookings for that email."}


def reschedule(booking_id, email, day, time):
    """Move a booking to a new free slot."""
    bookings = load()
    booking = find(bookings, booking_id, email)
    if not booking:
        return {"error": "No booking with that number and email."}
    if time not in free_slots(day).get("free", []):
        return {"error": "That time isn't free. Check free_slots again."}
    booking["day"], booking["time"] = day, time
    save(bookings)
    confirm(booking, "moved")
    return {"moved": booking}


def cancel(booking_id, email):
    """Cancel a booking. We keep it in the file, marked as cancelled."""
    bookings = load()
    booking = find(bookings, booking_id, email)
    if not booking:
        return {"error": "No booking with that number and email."}
    booking["status"] = "cancelled"
    save(bookings)
    confirm(booking, "cancelled")
    return {"cancelled": booking}


TOOLS = [
    tool_json("free_slots", "List the free times on one day.", {"day": "The day, as YYYY-MM-DD"}, ["day"]),
    tool_json("book", "Book an appointment, after the customer has confirmed every detail.",
              {"name": "The customer's name", "email": "The customer's email", "service": "Haircut, Colour or Beard trim",
               "day": "The day, as YYYY-MM-DD", "time": "A free time, like 14:00"}, ["name", "email", "service", "day", "time"]),
    tool_json("my_bookings", "List a customer's upcoming bookings, with the late fee for cancelling each one.", {"email": "The customer's email"}, ["email"]),
    tool_json("reschedule", "Move a booking to a new free time.",
              {"booking_id": "Like B103", "email": "The email on the booking", "day": "The new day, as YYYY-MM-DD",
               "time": "The new free time"}, ["booking_id", "email", "day", "time"]),
    tool_json("cancel", "Cancel a booking, after the customer has confirmed.",
              {"booking_id": "Like B103", "email": "The email on the booking"}, ["booking_id", "email"]),
]
TOOL_MAP = {"free_slots": free_slots, "book": book, "my_bookings": my_bookings, "reschedule": reschedule, "cancel": cancel}

PROMPT = f"""You book appointments for Studio Nora, a small hair salon. Be friendly and short.

## The salon
- Open {", ".join(OPEN_DAYS)}. Appointments start at {", ".join(HOURS)} and take up to one hour.
- Morning means 09:00 to 12:00. Afternoon means 14:00 to 16:00.
- Services and prices: {", ".join(f"{s} {p}" for s, p in SERVICES.items())}.

## Rules
- Always use free_slots before offering times. Never guess what's free.
- To book, you need a name, an email, a service, a day and a time.
- Never book, reschedule or cancel straight away. First repeat the details and ask "Shall I go ahead?".
  Only use the tool after the customer says yes.
- After booking, always give the customer their booking number, like B104.
- To reschedule or cancel, first use my_bookings to find the booking. It also shows the late_fee:
  if it's €10, tell the customer before they confirm a cancellation.
- Only help with bookings at Studio Nora."""


def chat(message, history):
    today = f"\n\nToday is {date.today():%A %Y-%m-%d}."
    return run_agent(PROMPT + today, history, message, TOOLS, TOOL_MAP)


if __name__ == "__main__":
    examples = ["Can I get a haircut on Thursday afternoon?", "I need to move my appointment", "What do you charge for colour?"]
    gr.ChatInterface(chat, title="Studio Nora: book an appointment", examples=examples).launch(theme=gr.themes.Soft(primary_hue="pink"))
