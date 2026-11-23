order = {"id": 1042, "item": "Ceramic vase", "status": "shipped"}

print(order["item"])                  # look up a value by its label
print(order.get("note", "no note"))   # a safe look-up, with a fallback

order["status"] = "delivered"         # change a value
order["rating"] = 5                   # add a new label
print(order)
