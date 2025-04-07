from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, ConfigDict
from enum import StrEnum

from models import Order


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


async def retrieve_all_orders(db: AsyncSession) -> list[OrderOut]:
    results = await db.execute(select(Order))
    orders = results.scalars().all()
    return [OrderOut.model_validate(order) for order in orders]


async def add_new_oder(db: AsyncSession, order: OrderIn) -> OrderOut:
    new_order = Order(**order.model_dump(exclude_none=True))
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return OrderOut.model_validate(new_order)
