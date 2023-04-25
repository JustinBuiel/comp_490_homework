from product import Product


def total_calculator(state: str, items: list[Product]) -> int:
    tax: float = 0
    taxed: bool = False
    total: int = 0

    match state:
        case "DE":
            tax = 0
        case "NJ":
            tax = .066
        case "PA":
            tax = .06
        case _:
            print("Invalid state format or no business in given state")
            return 0

    for item in items:

        item_total: int = int(round(item.unit_price * 100)) * item.quantity

        match item.type:
            case "etc":
                taxed = True
            case "WIC":
                taxed = False
            case "clothing":
                taxed = False
                if state == "NJ" and _is_fur(item.name):
                    taxed = True
        if taxed:
            total = total + item_total + (item_total * tax)
        else:
            total = total + item_total

    return int(round(total))


def _is_fur(name: str) -> bool:
    if "fur" in name.lower():
        return True
    return False
