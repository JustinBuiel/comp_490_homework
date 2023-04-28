from pydantic import StrictFloat, StrictInt, StrictStr, validator
from pydantic.dataclasses import dataclass


@dataclass(validate_on_init=True)
class Product:
    name: StrictStr
    type: StrictStr
    unit_price: StrictFloat
    quantity: StrictInt = 1

    @validator("name")
    def check_name(cls, value):
        if len("".join(value.split())) >= 1:
            return value
        else:
            raise ValueError("Name must be at least 1 real character")

    @validator("type")
    def check_type(cls, value):
        if value == "clothing" or value == "etc" or value == "WIC":
            return value
        else:
            raise ValueError("Type must be clothing, WIC or etc")

    @validator("unit_price")
    def check_price(cls, value):
        if value > 0.0:
            return value
        else:
            raise ValueError("Item price must be at least 1 cent")

    @validator("quantity")
    def check_quantity(cls, value):
        if value > 0:
            return value
        else:
            raise ValueError("Item quantity must be a positive int")
