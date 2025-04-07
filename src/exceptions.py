from fastapi import HTTPException


class OderError(HTTPException):
    """Base exception for order related errors"""

    pass


class OrderNotFoundError(OderError):
    def __init__(self, order_id=None):
        message = (
            "Order not found"
            if order_id is None
            else f"Order with id {order_id} not found"
        )
        super().__init__(status_code=404, detail=message)
