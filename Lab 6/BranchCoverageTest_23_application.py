
from shopping_cart import shipping_fee


def test_shipping_fee_non_prime_express():
    assert shipping_fee(100, False, True) == 140

