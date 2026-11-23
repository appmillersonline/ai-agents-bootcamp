"""Sara's refund and expense rules, from the shop handbook, as plain code. The model never decides; these functions do."""
REFUND_LIMIT = 20   # euros: up to this, approve straight away; above it, Sara decides
EXPENSE_LIMIT = 20  # euros: staff expenses, same idea
RETURN_DAYS = 30    # unused items can be returned within 30 days of delivery


def check(form) -> tuple[str, str]:
    """Return (path, rule): path is "approve", "ask_sara" or "reject"."""
    if form.kind == "refund":
        if form.is_candle and form.used:
            return "reject", "Candles can only be returned unopened and unused."
        if form.reason == "changed_mind" and form.days_since_delivery is not None and form.days_since_delivery > RETURN_DAYS:
            return "reject", f"Returns are accepted within {RETURN_DAYS} days of delivery."
        if form.reason == "damaged" and not form.has_photo:
            return "reject", "Damaged items need one photo of the damage first: ask the customer for it."
        if form.amount_eur > REFUND_LIMIT:
            return "ask_sara", f"Refunds over {REFUND_LIMIT} euros need Sara's approval."
        return "approve", f"Refunds up to {REFUND_LIMIT} euros can be done straight away."
    if form.amount_eur > EXPENSE_LIMIT:
        return "ask_sara", f"Expenses over {EXPENSE_LIMIT} euros need Sara's approval."
    return "approve", f"Expenses up to {EXPENSE_LIMIT} euros are paid back straight away."
