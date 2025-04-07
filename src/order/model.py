from pydantic import BaseModel, ConfigDict
from enum import StrEnum


class CoffeType(StrEnum):
    espresso = "Espresso"
    latte = "Latte"
    cappuccino = "Cappuccino"
    americano = "Americano"


class CoffeeSize(StrEnum):
    small = "Small"
    medium = "Medium"
    large = "Large"


class OrderIn(BaseModel):
    coffee_name: CoffeType
    size: CoffeeSize
    quantity: int


class OrderOut(OrderIn):
    id: int

    model_config = ConfigDict(from_attributes=True)
