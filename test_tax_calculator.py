import pytest
from pydantic import ValidationError
from product import Product
from tax_calculator import total_calculator


def test_mixed_cart():
    cart1: list = [
        Product("Coat", "clothing", 59.99),
        Product("Fur Scarf", "clothing", 24.99, 2),
        Product("Milk - 1 Gallon", "WIC", 2.98),
        Product("Sunglasses - Polarized", "etc", 5.99)
    ]

    assert total_calculator("DE", cart1) == 11894
    assert total_calculator("NJ", cart1) == 12263
    assert total_calculator("PA", cart1) == 11930


def test_etc_only():
    cart2: list = [
        Product("Xbox Series X", "etc", 499.99),
        Product("Xbox Elite Controller ", "etc", 249.99),
        Product("Halo Infinite", "etc", 69.99)
    ]

    assert total_calculator("DE", cart2) == 81997
    assert total_calculator("NJ", cart2) == 87409
    assert total_calculator("PA", cart2) == 86917


def test_clothing_only():
    cart3: list = [
        Product("Jeans", "clothing", 49.99, 2),
        Product("Socks- 6 Pack", "clothing", 6.99),
        Product("winter coat - fur", "clothing", 99.99)
    ]

    assert total_calculator("DE", cart3) == 20696
    assert total_calculator("NJ", cart3) == 21356
    assert total_calculator("PA", cart3) == 20696


def test_wic_only():
    cart4: list = [
        Product("1/2 Gallon Milk", "WIC", 1.59),
        Product("Wheat Bread", "WIC", 3.29),
        Product("Honey Nut Cheerios", "WIC", 7.99)
    ]

    assert total_calculator("DE", cart4) == 1287
    assert total_calculator("NJ", cart4) == 1287
    assert total_calculator("PA", cart4) == 1287


def test_errors(capfd):
    cart5: list = [
        Product("Product", "etc", 0.99)
    ]

    assert total_calculator("NY", cart5) == 0
    out, err = capfd.readouterr()
    assert out == "Invalid state format or no business in given state\n"

    assert total_calculator("Penn", cart5) == 0
    out, err = capfd.readouterr()
    assert out == "Invalid state format or no business in given state\n"

    # name must be string
    with pytest.raises(ValidationError) as exception_info:
        Product(2, "etc", 119.99)
    assert exception_info.type == ValidationError

    # type must be WIC, clothing or etc
    with pytest.raises(ValidationError) as exception_info:
        Product("product", "food", 119.99)
    assert exception_info.type is ValidationError

    # price must be float
    with pytest.raises(ValidationError) as exception_info:
        Product("product", "etc", 120)
    assert exception_info.type is ValidationError

    # quantity must be int
    with pytest.raises(ValidationError) as exception_info:
        Product("product", "etc", 119.99, 1.0)
    assert exception_info.type is ValidationError

    # This next set worked when i was using pydantic.validate_arguments on the funciton but
    # I didn't like that so I've changed to manual validation instead so no conversion happens

    # i thought these would be error but the validate_arguments will convert these to a Product
    # cart6 = [
    #     ["Xbox", "etc", 499.99],
    #     ("Xbox", "etc", 499.99),
    #     {"name": "Xbox", "type": "etc", "unit_price": 499.99}
    # ]

    # assert total_calculator("DE", cart6) == 149997
    # assert total_calculator("NJ", cart6) == 159897
    # assert total_calculator("PA", cart6) == 158997

    with pytest.raises(TypeError) as exception_info:
        total_calculator(3, cart5)  # NJ was the 3rd state
    assert exception_info.type is TypeError

    cart7 = [
        "Xbox",
        "etc",
        499.99
    ]

    with pytest.raises(TypeError) as exception_info:
        total_calculator("DE", cart7)
    assert exception_info.type is TypeError

    cart8 = [
        ["Xbox", "etc", 499.99]
    ]

    with pytest.raises(TypeError) as exception_info:
        total_calculator("DE", cart8)
    assert exception_info.type is TypeError

    cart9 = [
        ("Xbox", "etc", 499.99)
    ]

    with pytest.raises(TypeError) as exception_info:
        total_calculator("DE", cart9)
    assert exception_info.type is TypeError

    cart10 = [
        {"name": "Xbox", "type": "etc", "unit_price": 499.99}
    ]

    with pytest.raises(TypeError) as exception_info:
        total_calculator("DE", cart10)
    assert exception_info.type is TypeError

    single_item_purchase = Product("Xbox", "etc", 499.99)

    # still want a cart (list) even for single items
    with pytest.raises(TypeError) as exception_info:
        total_calculator("DE", single_item_purchase)
    assert exception_info.type is TypeError
