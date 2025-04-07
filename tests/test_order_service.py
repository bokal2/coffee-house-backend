import pytest

from src.order.model import OrderIn, CoffeeSize, CoffeType
from src.order.service import add_new_oder


@pytest.mark.asyncio
async def test_create_order(db_session):
    order = OrderIn(
        coffee_name=CoffeType.espresso,
        size=CoffeeSize.small,
        quantity=3,
    )

    new_order = await add_new_oder(db=db_session, order=order)
    assert new_order.coffee_name == "Espresso"
