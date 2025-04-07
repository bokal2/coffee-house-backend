from fastapi import FastAPI, Depends, Request, Response
import logging
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from prometheus_fastapi_instrumentator import Instrumentator

from db.session import engine
from db.items import OrderIn, retrieve_all_orders, add_new_oder
from db.core import get_db
from models import Base
from core.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized.")

    yield  # App runs here

    print("App shutting down.")


app = FastAPI(
    title="Coffee House",
    description=("Coffee House is a simple API that allows you to order coffee."),
    lifespan=lifespan,
)

# Configure allowed origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_and_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id

    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host,
            "headers": dict(request.headers),
        },
    )

    response: Response = await call_next(request)

    logger.info(
        "Outgoing response",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "url": str(request.url),
        },
    )

    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


Instrumentator().instrument(app).expose(app)


@app.get("/orders")
async def get_orders(db: AsyncSession = Depends(get_db)):
    orders = await retrieve_all_orders(db)
    return orders


@app.post("/orders")
async def create_order(order: OrderIn, db: AsyncSession = Depends(get_db)):
    return await add_new_oder(db, order)
