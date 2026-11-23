"""Gift card system for Sara's candle shop."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import random
import re


class GiftCards:
    _CODE_RE = re.compile(r"^SARA-\d{4}$")
    _MAX_CODE_ATTEMPTS = 10_000

    def __init__(self) -> None:
        self._cards = {}

    def issue_card(self, amount) -> str:
        amount = self._validate_amount(amount)
        card_code = self._generate_card_code()
        self._cards[card_code] = {
            "code": card_code,
            "balance": amount,
            "cancelled": False,
            "history": [],
        }
        self._record_event(card_code, "issued", amount, amount)
        return card_code

    def spend(self, card_code: str, amount) -> bool:
        self._validate_card_code(card_code)
        amount = self._validate_amount(amount)
        card = self._get_card(card_code)
        if card["cancelled"]:
            raise PermissionError("card is cancelled")
        if amount <= card["balance"]:
            card["balance"] -= amount
            self._record_event(card_code, "spent", amount, card["balance"])
            return True
        self._record_event(card_code, "refused", amount, card["balance"])
        return False

    def get_balance(self, card_code: str):
        self._validate_card_code(card_code)
        return self._get_card(card_code)["balance"]

    def get_history(self, card_code: str) -> list[dict]:
        self._validate_card_code(card_code)
        history = self._get_card(card_code)["history"]
        return [dict(entry) for entry in history]

    def cancel_card(self, card_code: str) -> None:
        self._validate_card_code(card_code)
        card = self._get_card(card_code)
        if card["cancelled"]:
            raise ValueError("card is already cancelled")
        card["cancelled"] = True
        self._record_event(card_code, "cancelled", None, card["balance"])

    def _generate_card_code(self) -> str:
        for _ in range(self._MAX_CODE_ATTEMPTS):
            code = f"SARA-{random.randint(0, 9999):04d}"
            if code not in self._cards:
                return code
        raise RuntimeError("could not generate a unique card code")

    def _validate_card_code(self, card_code: str) -> None:
        if not isinstance(card_code, str):
            raise ValueError("card code must be a string")
        if not self._CODE_RE.fullmatch(card_code):
            raise ValueError("invalid card code format")

    def _validate_amount(self, amount):
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError("invalid amount") from exc
        if value <= 0:
            raise ValueError("amount must be greater than zero")
        return value

    def _get_card(self, card_code: str) -> dict:
        self._validate_card_code(card_code)
        try:
            return self._cards[card_code]
        except KeyError as exc:
            raise KeyError(card_code) from exc

    def _record_event(self, card_code: str, event_type: str, amount, balance) -> None:
        if event_type not in {"issued", "spent", "refused", "cancelled"}:
            raise ValueError("invalid event type")
        if event_type == "cancelled":
            if amount is not None:
                raise ValueError("cancelled events must not have an amount")
        else:
            amount = self._validate_amount(amount)
        self._cards[card_code]["history"].append(
            {"type": event_type, "amount": amount, "balance": balance}
        )
