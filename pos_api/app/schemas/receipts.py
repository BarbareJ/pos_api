from enum import Enum
from typing import List

from pydantic import BaseModel


class ReceiptStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class ReceiptItemResponse(BaseModel):
    id: str
    quantity: int
    price: int
    total: int


class ReceiptResponse(BaseModel):
    id: str
    status: ReceiptStatus
    products: List[ReceiptItemResponse] = []
    total: int

    class Config:
        orm_mode = True


class ReceiptCreate(BaseModel):
    pass


class ReceiptAddProductRequest(BaseModel):
    id: str
    quantity: int


class ReceiptCloseRequest(BaseModel):
    status: ReceiptStatus


class ReceiptReadResponse(BaseModel):
    receipt: ReceiptResponse


class ReceiptCreateResponse(BaseModel):
    receipt: ReceiptResponse
