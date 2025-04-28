import uuid
from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class ReceiptStatus(str, PyEnum):
    OPEN = "open"
    CLOSED = "closed"


class Unit(Base): # type: ignore[misc]
    __tablename__ = "units"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)


class Product(Base): # type: ignore[misc]
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=generate_uuid)
    unit_id = Column(String, ForeignKey("units.id"), nullable=False)
    name = Column(String, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)

    unit = relationship("Unit")


class Receipt(Base): # type: ignore[misc]
    __tablename__ = "receipts"
    id = Column(String, primary_key=True, default=generate_uuid)
    status: "ReceiptStatus"
    status = Column(Enum(ReceiptStatus), nullable=False, default=ReceiptStatus.OPEN)
    total = Column(Integer, nullable=False, default=0)
    products = relationship(
        "ReceiptItem", back_populates="receipt", cascade="all, delete-orphan"
    )


class ReceiptItem(Base): # type: ignore[misc]
    __tablename__ = "receipt_items"
    id = Column(String, primary_key=True, default=generate_uuid)
    receipt_id = Column(String, ForeignKey("receipts.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_sale = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)

    receipt = relationship("Receipt", back_populates="products")
    product = relationship("Product")
