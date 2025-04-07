import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "coffee_shop")
DB_PORT = os.getenv("DB_PORT", "5432")

# URL-encode password to handle special characters
ENCODED_PASSWORD = quote_plus(DB_PASSWORD)

database_url = (
    f"postgresql+asyncpg://{DB_USER}:{ENCODED_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


print(f"--- Connecting to database at {database_url} ---")
# Create async engine
engine = create_async_engine(database_url, echo=True)

Base = declarative_base()

# Create async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
