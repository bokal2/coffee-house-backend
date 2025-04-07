import pytest


@pytest.mark.asyncio
async def test_create_order(client):
    response = await client.post(
        "/orders/",
        json={
            "coffee_name": "Espresso",
            "size": "Small",
            "quantity": 3,
        },
    )

    assert response.status_code == 201
    data = response.json()
    # assert data["item_name"] == "Test Product"
