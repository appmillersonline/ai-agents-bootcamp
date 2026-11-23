"""What goes wrong, and how to catch it: the SDK raises a different error for each problem."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

TRIES = [("claude-opus-9", 1000), ("claude-opus-5-5", 20), ("claude-opus-5-5", 1000)]  # a typo, a tiny limit, fine

for model, limit in TRIES:
    try:
        response = client.messages.create(model=model, max_tokens=limit,
                                          messages=[{"role": "user", "content": "Say hi to Sara in three words."}])
        text = next((b.text for b in response.content if b.type == "text"), "(no text)")
        print(f"{model}, max_tokens={limit}: {text}  [stop: {response.stop_reason}]")
    except anthropic.NotFoundError:
        print(f"{model}: not found (404). Check the model name")
    except anthropic.AuthenticationError:
        print("Your API key is wrong. Check .env")
    except anthropic.RateLimitError:
        print("Too many requests. Wait a moment and try again")
    except anthropic.APIConnectionError:
        print("No internet connection")
