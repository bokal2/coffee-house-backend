from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.order.model import OrderIn, OrderOut
from src.entities.order import Order
from src.exceptions import OrderNotFoundError


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


async def get_order(db: AsyncSession, order_id: int) -> OrderOut:
    result = await db.execute(select(Order).filter(id=order_id))
    order = result.scalars().one()
    if not order:
        raise OrderNotFoundError(order_id=order_id)
    return OrderOut.model_validate(order)
