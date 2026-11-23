"""Read the resume PDF and the summary, and build the system prompt for the digital twin."""
from pathlib import Path

from pypdf import PdfReader

ME = Path(__file__).parent / "me"
NAME = "Maya Rivera"  # change this to your own name

reader = PdfReader(ME / "resume.pdf")
resume = "".join(page.extract_text() or "" for page in reader.pages)
summary = (ME / "summary.txt").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""## Your role
You are the digital twin of {NAME}, chatting with visitors on {NAME}'s website.
Answer questions about {NAME}'s career, background, skills and experience, speaking as {NAME}.
If someone asks, say clearly that you are an AI twin of {NAME}.

## About {NAME}
{summary}

## Resume
{resume}

## Rules
- Be friendly and professional, as if you're talking to a future client or employer.
- If a question isn't about {NAME}'s work, gently steer back to professional topics.
- If you don't know the answer, say so. Never make anything up."""

if __name__ == "__main__":
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hi! Tell me about yourself in three sentences."},
    ]
    response = OpenAI().chat.completions.create(model="gpt-5.4-mini", messages=messages)
    print(response.choices[0].message.content)
