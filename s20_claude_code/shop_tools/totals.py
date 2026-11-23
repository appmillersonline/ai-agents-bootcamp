"""Order totals for Sara's shop (sample data)."""

FREE_SHIPPING_FROM = 40.0
SHIPPING = 4.5


def order_total(prices: list[float], discount: float = 0.0) -> float:
    """Sum the items, take off the discount (0.1 = 10 %), add shipping under 40 euros."""
    subtotal = sum(prices)
    subtotal = subtotal - discount
    if subtotal > FREE_SHIPPING_FROM:
        return round(subtotal, 2)
    return round(subtotal + SHIPPING, 2)
