from totals import order_total


def test_small_order_pays_shipping():
    assert order_total([12.0, 8.0]) == 24.5


def test_ten_percent_discount():
    assert order_total([50.0], discount=0.1) == 45.0


def test_exactly_forty_ships_free():
    assert order_total([25.0, 15.0]) == 40.0
