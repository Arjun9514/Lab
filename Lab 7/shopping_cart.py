ZONES = {
    "1": "North", "2": "North",
    "3": "West", "4": "West",
    "5": "South", "6": "South",
    "7": "East", "8": "East"
}


def cart_total(cart):
    if not isinstance(cart, str) or not cart.strip():
        return 0

    total = 0

    for item in cart.split(","):
        try:
            name, rest = item.strip().split(":")
            price, qty = rest.split("x")

            if not name.strip():
                continue

            price = int(price)
            qty = int(qty)

            if price < 0 or qty < 0:
                continue

            total += price * qty

        except (ValueError, TypeError):
            continue

    return total


def promo_percent(code):
    if not isinstance(code, str):
        return 0

    code = code.strip().upper()

    if not code.startswith("OFF"):
        return 0

    try:
        percent = int(code[3:])

        if 0 <= percent <= 100:
            return percent

    except ValueError:
        pass

    return 0


def delivery_zone(pincode):
    if not isinstance(pincode, str):
        return "Invalid Pincode"

    pincode = pincode.strip()

    if len(pincode) != 6 or not pincode.isascii() or not pincode.isdigit():
        return "Invalid Pincode"

    return ZONES.get(pincode[0], "Invalid Pincode")


def main():
    print("==== Running cart_total ====")
    user_input = input(
        "Enter cart as name:pricexqty CSV "
        "(e.g. pen:10x2,book:250x1): "
    )
    result = cart_total(user_input)
    print("Cart Total:", result)

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    print("Discount Percent:", result)

    print("\n==== Running delivery_zone ====")
    user_input = input(
        "Enter a 6 digit pincode (e.g. 560085): "
    )
    result = delivery_zone(user_input)
    print("Delivery Zone:", result)


if __name__ == "__main__":
    main()
