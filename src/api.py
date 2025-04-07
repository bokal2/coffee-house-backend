from fastapi import FastAPI
from src.order.controller import router as order_router


def register_routes(app: FastAPI):
    app.include_router(order_router)
