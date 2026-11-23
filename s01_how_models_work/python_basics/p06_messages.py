# A list of dictionaries: exactly the shape you send to an AI model
messages = [
    {"role": "user", "content": "Where is my order?"},
    {"role": "assistant", "content": "It shipped today!"},
]

messages.append({"role": "user", "content": "Great, thanks!"})

for message in messages:
    print(message["role"], "says:", message["content"])
