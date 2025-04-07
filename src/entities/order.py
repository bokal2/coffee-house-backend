from datetime import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime
from src.db.core import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    coffee_name = Column(String)
    size = Column(String)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=dt.utcnow)
