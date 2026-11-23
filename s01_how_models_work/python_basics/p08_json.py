import json

# AI models and tools often pass data around as JSON text
text = '{"order_id": 1042, "status": "shipped", "items": ["vase", "candle"]}'

data = json.loads(text)               # JSON text becomes a Python dictionary
print(data["status"])
print(len(data["items"]), "items")

print(json.dumps(data, indent=2))     # and back again, as neat JSON text
