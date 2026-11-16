import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ITEM TOTAL TESTS

def test_item_total_normal_food():
    assert item_total("food", 100, 2) == 210


def test_item_total_bulk_discount():
    assert item_total("electronics", 100, 10) == 1062


def test_item_total_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        item_total("furniture", 100, 2)


def test_item_total_invalid_price():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -100, 2)


def test_item_total_invalid_quantity():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, 0)


# CART DISCOUNT TESTS

def test_cart_discount_high_value_prime_coupon():
    assert cart_discount(5000, True, "FLAT10") == 1100


def test_cart_discount_medium_value():
    assert cart_discount(2000, False, "NONE") == 200


def test_cart_discount_low_value():
    assert cart_discount(1000, False, "NONE") == 0


# SHIPPING FEE TESTS

def test_shipping_fee_below_threshold():
    assert shipping_fee(100, False, False) == 40


def test_shipping_fee_above_threshold():
    assert shipping_fee(1000, False, False) == 0


def test_shipping_fee_prime_express():
    assert shipping_fee(100, True, True) == 50
