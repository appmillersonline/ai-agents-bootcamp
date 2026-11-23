def greet(name, shop="Sara's Shop"):
    """Return a thank-you message for one customer."""
    return f"Hi {name}, thanks for shopping at {shop}!"


print(greet("Maya"))
print(greet("Leo", shop="Candle Corner"))
