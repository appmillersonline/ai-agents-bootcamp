import pytest

from giftcards import GiftCards


@pytest.fixture

def giftcards():
    return GiftCards()


def test_issue_card_creates_code_balance_and_history(giftcards):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("giftcards.random.randint", lambda a, b: 1234)
        code = giftcards.issue_card("25.50")

    assert code == "SARA-1234"
    assert giftcards.get_balance(code) == pytest.approx(25.50)
    history = giftcards.get_history(code)
    assert history == [
        {"type": "issued", "amount": pytest.approx(25.50), "balance": pytest.approx(25.50)}
    ]


def test_spend_reduces_balance_and_records_history(giftcards):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("giftcards.random.randint", lambda a, b: 1234)
        code = giftcards.issue_card(40)

    assert giftcards.spend(code, 15) is True
    assert giftcards.get_balance(code) == pytest.approx(25)
    assert giftcards.get_history(code)[-1] == {"type": "spent", "amount": pytest.approx(15), "balance": pytest.approx(25)}


def test_spend_refused_when_amount_exceeds_balance_and_nothing_is_taken(giftcards):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("giftcards.random.randint", lambda a, b: 1234)
        code = giftcards.issue_card(10)

    assert giftcards.spend(code, 11) is False
    assert giftcards.get_balance(code) == pytest.approx(10)
    assert giftcards.get_history(code)[-1] == {"type": "refused", "amount": pytest.approx(11), "balance": pytest.approx(10)}


def test_cancelled_card_cannot_be_spent_and_history_records_cancellation(giftcards):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("giftcards.random.randint", lambda a, b: 1234)
        code = giftcards.issue_card(20)

    giftcards.cancel_card(code)
    assert giftcards.get_history(code)[-1] == {"type": "cancelled", "amount": None, "balance": pytest.approx(20)}
    with pytest.raises(PermissionError):
        giftcards.spend(code, 1)
    assert giftcards.get_balance(code) == pytest.approx(20)


def test_every_amount_must_be_more_than_zero(giftcards):
    with pytest.raises(ValueError):
        giftcards.issue_card(0)
    with pytest.raises(ValueError):
        giftcards.issue_card(-1)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("giftcards.random.randint", lambda a, b: 1234)
        code = giftcards.issue_card(5)

    with pytest.raises(ValueError):
        giftcards.spend(code, 0)
    with pytest.raises(ValueError):
        giftcards.spend(code, -1)


def test_invalid_card_code_rejected(giftcards):
    with pytest.raises(ValueError):
        giftcards.get_balance("bad-code")
    with pytest.raises(ValueError):
        giftcards.get_history(123)


def test_unknown_card_code_raises_key_error(giftcards):
    with pytest.raises(KeyError):
        giftcards.get_balance("SARA-1234")


def test_cancelling_twice_raises_value_error(giftcards):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("giftcards.random.randint", lambda a, b: 1234)
        code = giftcards.issue_card(5)

    giftcards.cancel_card(code)
    with pytest.raises(ValueError):
        giftcards.cancel_card(code)
