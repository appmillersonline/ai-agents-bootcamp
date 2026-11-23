"""Tests for the rules: no model, no internet, they run in a second."""
from approvals import RequestForm
from rules import check


def form(**changes):
    base = dict(kind="refund", who="Test", item="mug", order="1", amount_eur=14, reason="damaged",
                has_photo=True, is_candle=False, used=False, days_since_delivery=None)
    return RequestForm(**{**base, **changes})


def test_exactly_the_limit_is_approved():
    assert check(form(amount_eur=20))[0] == "approve"


def test_one_cent_over_goes_to_sara():
    assert check(form(amount_eur=20.01))[0] == "ask_sara"


def test_opened_candle_is_rejected():
    assert check(form(item="candle", is_candle=True, used=True))[0] == "reject"


def test_return_after_31_days_is_rejected():
    assert check(form(reason="changed_mind", days_since_delivery=31))[0] == "reject"


def test_return_on_day_30_is_fine():
    assert check(form(reason="changed_mind", days_since_delivery=30))[0] == "approve"


def test_big_expense_goes_to_sara():
    assert check(form(kind="expense", reason="staff_purchase", amount_eur=25))[0] == "ask_sara"


def test_damaged_without_photo_is_not_approved():
    assert check(form(has_photo=False))[0] != "approve"
