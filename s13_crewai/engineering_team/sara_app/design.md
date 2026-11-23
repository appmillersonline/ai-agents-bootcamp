# Design for `giftcards.py`

## Module purpose
`giftcards.py` defines one class, `GiftCards`, to manage Sara’s candle shop gift cards.

The class supports:
- issuing a gift card with a positive euro balance
- generating a short code like `SARA-1234`
- spending from a card
- refusing overspend attempts without changing the balance
- checking current balance
- viewing card history
- cancelling a card
- blocking spending on cancelled cards

No code is defined here; this is the behavior contract.

---

## Class: `GiftCards`

### Responsibility
Manage an in-memory collection of gift cards and their event histories.

Each gift card has:
- a unique card code
- a current balance in euros
- a status: active or cancelled
- a history of events

Each history event records:
- event type: `issued`, `spent`, `refused`, or `cancelled`
- amount in euros when applicable
- resulting balance after the event when applicable

---

## Data rules

### Card code format
- Every issued card code must be a string in the form `SARA-1234`.
- `SARA-` is fixed and uppercase.
- `1234` means exactly 4 digits.
- Codes must be unique within one `GiftCards` instance.

### Amount rules
- Every amount must be greater than zero.
- Zero is invalid.
- Negative amounts are invalid.
- Amounts are in euros.
- The implementation should use a money-safe numeric representation consistently. The interface accepts an amount value, but invalid numeric values must be rejected.

### Spending rules
- A spend request with amount greater than the current balance is refused.
- On refusal, the card balance does not change.
- A refused spend must still be written to the card history.

### Cancellation rules
- A cancelled card cannot be spent.
- Cancelling a card does not erase its history.
- Balance inquiry and history inquiry remain allowed for cancelled cards.

---

## Errors

The module should raise only clear built-in exceptions unless the developer later wraps them.

### `ValueError`
Raise when:
- an amount is not greater than zero
- a card code format is invalid
- a card is already cancelled and cancellation is requested again
- an amount value is not acceptable as a euro amount

### `KeyError`
Raise when:
- a requested card code does not exist

### `RuntimeError`
Raise when:
- a unique card code cannot be generated after a bounded number of attempts

### `PermissionError`
Raise when:
- spending is attempted on a cancelled card

---

## Public methods

### `__init__(self) -> None`
Create an empty gift card manager.

#### Arguments
- none

#### Returns
- `None`

#### Behavior
- Initializes storage for all cards and their histories.
- Starts with no issued cards.

#### Raises
- No errors in normal use.

---

### `issue_card(self, amount) -> str`
Issue a new gift card with a starting balance.

#### Arguments
- `amount`: starting balance in euros; must be greater than zero

#### Returns
- `str`: the new gift card code in the format `SARA-1234`

#### Behavior
- Validates that `amount` is more than zero.
- Generates a unique code in the required format.
- Creates a new active card with the given starting balance.
- Records a history event of type `issued` with that amount.
- The resulting balance after the event is the starting balance.

#### Raises
- `ValueError`:
  - if `amount` is zero, negative, or otherwise invalid
- `RuntimeError`:
  - if a unique card code cannot be generated

---

### `spend(self, card_code: str, amount) -> bool`
Attempt to spend from a gift card.

#### Arguments
- `card_code`: the gift card code
- `amount`: amount in euros to spend; must be greater than zero

#### Returns
- `bool`:
  - `True` if the spend succeeds
  - `False` if the spend is refused because the amount is greater than the available balance

#### Behavior
- Validates `card_code` format.
- Confirms the card exists.
- Validates that `amount` is more than zero.
- If the card is cancelled, spending is not allowed.
- If `amount` is less than or equal to current balance:
  - deducts the amount from the balance
  - records a `spent` history event
  - returns `True`
- If `amount` is greater than current balance:
  - leaves balance unchanged
  - records a `refused` history event with the attempted amount
  - returns `False`

#### Raises
- `ValueError`:
  - if `card_code` format is invalid
  - if `amount` is zero, negative, or otherwise invalid
- `KeyError`:
  - if `card_code` does not exist
- `PermissionError`:
  - if the card is cancelled

---

### `get_balance(self, card_code: str)`
Return the current balance of a card.

#### Arguments
- `card_code`: the gift card code

#### Returns
- current balance in euros

#### Behavior
- Validates `card_code` format.
- Confirms the card exists.
- Returns the current balance.
- Works for both active and cancelled cards.

#### Raises
- `ValueError`:
  - if `card_code` format is invalid
- `KeyError`:
  - if `card_code` does not exist

---

### `get_history(self, card_code: str) -> list[dict]`
Return the full event history for a card.

#### Arguments
- `card_code`: the gift card code

#### Returns
- `list[dict]`: a new list of history entries in chronological order, oldest first

#### Behavior
- Validates `card_code` format.
- Confirms the card exists.
- Returns the card’s history without allowing callers to mutate internal storage directly.
- History includes all events for the card:
  - `issued`
  - `spent`
  - `refused`
  - `cancelled`

#### History entry shape
Each returned dict must contain:
- `type: str`
  - one of `issued`, `spent`, `refused`, `cancelled`
- `amount`
  - euro amount for `issued`, `spent`, and `refused`
  - `None` for `cancelled`
- `balance`
  - resulting card balance after the event
  - for `refused`, this is the unchanged balance after refusal
  - for `cancelled`, this is the balance at cancellation time

#### Raises
- `ValueError`:
  - if `card_code` format is invalid
- `KeyError`:
  - if `card_code` does not exist

---

### `cancel_card(self, card_code: str) -> None`
Cancel an existing card.

#### Arguments
- `card_code`: the gift card code

#### Returns
- `None`

#### Behavior
- Validates `card_code` format.
- Confirms the card exists.
- Marks the card as cancelled.
- Records a `cancelled` history event.
- Does not change the balance.

#### Raises
- `ValueError`:
  - if `card_code` format is invalid
  - if the card is already cancelled
- `KeyError`:
  - if `card_code` does not exist

---

## Private helper methods

These are part of the design and should be implemented as non-public methods.

### `_generate_card_code(self) -> str`
Generate a unique gift card code.

#### Arguments
- none

#### Returns
- `str`: a unique code in the format `SARA-1234`

#### Behavior
- Generates a code with the required prefix and exactly 4 digits.
- Checks for uniqueness against existing cards.
- Retries up to a fixed maximum number of attempts.

#### Raises
- `RuntimeError`:
  - if no unique code is found within the attempt limit

---

### `_validate_card_code(self, card_code: str) -> None`
Validate card code format.

#### Arguments
- `card_code`: candidate card code

#### Returns
- `None`

#### Behavior
- Accepts only strings in the exact format `SARA-1234`.

#### Raises
- `ValueError`:
  - if the code is not a string
  - if the code does not match the required format

---

### `_validate_amount(self, amount)`
Validate a euro amount.

#### Arguments
- `amount`: candidate amount

#### Returns
- validated amount in the module’s chosen money-safe representation

#### Behavior
- Rejects missing, non-numeric, zero, and negative values.
- Ensures the amount is usable by the rest of the class.
- Ensures all public methods work with one consistent amount representation.

#### Raises
- `ValueError`:
  - if the amount is not a valid positive euro amount

---

### `_get_card(self, card_code: str) -> dict`
Fetch internal card data for an existing card.

#### Arguments
- `card_code`: the gift card code

#### Returns
- `dict`: internal card record

#### Behavior
- Assumes code format has already been validated or validates it before lookup.
- Returns the internal stored record for the card.

#### Raises
- `ValueError`:
  - if `card_code` format is invalid
- `KeyError`:
  - if `card_code` does not exist

---

### `_record_event(self, card_code: str, event_type: str, amount, balance) -> None`
Append one event to a card’s history.

#### Arguments
- `card_code`: the gift card code
- `event_type`: one of `issued`, `spent`, `refused`, `cancelled`
- `amount`: event amount, or `None` for cancellation
- `balance`: resulting balance after the event

#### Returns
- `None`

#### Behavior
- Adds one event to the end of the card’s history.
- Preserves chronological order.
- Stores exactly the fields returned by `get_history`.

#### Raises
- `ValueError`:
  - if `event_type` is not one of the allowed values
  - if `amount` is invalid for the given event type

---

## Internal card record design

Each card should be stored internally with at least:
- `code: str`
- `balance`: current euro balance
- `cancelled: bool`
- `history: list[dict]`

---

## Required method behavior examples

### Issue
- `issue_card(50)` returns something like `SARA-1234`
- balance is 50
- history is:
  - `issued`, amount 50, balance 50

### Successful spend
- card balance 50
- `spend(code, 20)` returns `True`
- new balance is 30
- history adds:
  - `spent`, amount 20, balance 30

### Refused spend
- card balance 30
- `spend(code, 40)` returns `False`
- balance remains 30
- history adds:
  - `refused`, amount 40, balance 30

### Cancelled card
- `cancel_card(code)` marks the card cancelled
- history adds:
  - `cancelled`, amount `None`, balance current balance
- later `spend(code, 5)` raises `PermissionError`

---

## Summary of public API

```text
class GiftCards:
    __init__(self) -> None
    issue_card(self, amount) -> str
    spend(self, card_code: str, amount) -> bool
    get_balance(self, card_code: str)
    get_history(self, card_code: str) -> list[dict]
    cancel_card(self, card_code: str) -> None
```

This design satisfies Sara’s requirements for issuing, spending, refusal handling, balance checks, history tracking, cancellation, and positive-only amounts.