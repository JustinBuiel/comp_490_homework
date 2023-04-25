from pydantic.dataclasses import dataclass
from pydantic import validator, StrictFloat, StrictInt, StrictStr


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
            raise ValueError
