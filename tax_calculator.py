from product import Product


def total_calculator(state: str, items: list[Product]) -> int:

    state = _validate_state(state)
    _validate_cart(items)

    tax_percentage: float = 0
    is_product_taxed: bool = False
    final_total: int = 0

    match state:
        case "DE":
            tax_percentage = 1.0
        case "NJ":
            tax_percentage = 1.066
        case "PA":
            tax_percentage = 1.06
        case _:
            print("Invalid state format or no business in given state")
            return 0

    for item in items:

        item_total: int = int(round(item.unit_price * 100)) * item.quantity

        match item.type:
            case "etc":
                is_product_taxed = True
            case "WIC":
                is_product_taxed = False
            case "clothing":
                is_product_taxed = False
                if state == "NJ" and _is_fur(item.name):
                    is_product_taxed = True
        if is_product_taxed:
            final_total = final_total + (item_total * tax_percentage)
        else:
            final_total = final_total + item_total

    return int(round(final_total))


def _is_fur(name: str) -> bool:
    if "fur" in name.lower():
        return True
    return False


def _validate_state(state: str):
    if isinstance(state, str):
        return state.upper()
    raise TypeError("State must be str")


def _validate_cart(cart: list[Product]):
    if not isinstance(cart, list):
        raise TypeError("Must have a list as a container for the items")
    for item in cart:
        if not isinstance(item, Product):
            raise TypeError("Items must be Products")
