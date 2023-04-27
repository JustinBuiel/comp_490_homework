from pydantic import StrictFloat, StrictInt, StrictStr, validator
from pydantic.dataclasses import dataclass


@dataclass(validate_on_init=True)
class Product:
    name: StrictStr
    type: StrictStr
    unit_price: StrictFloat
    quantity: StrictInt = 1

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
