from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db
from src.order.model import OrderIn
from src.order.service import retrieve_all_orders, add_new_oder
from src.rate_limiting import limiter

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def get_orders(request: Request, db: AsyncSession = Depends(get_db)):
    orders = await retrieve_all_orders(db)
    return orders


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderIn, db: AsyncSession = Depends(get_db)):
    return await add_new_oder(db, order)
