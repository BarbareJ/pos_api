from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Product, Receipt, Unit
from app.repositories.products import ProductRepository
from app.repositories.receipts import ReceiptRepository
from app.repositories.units import UnitRepository
from app.services.products import ProductService
from app.services.receipts import ReceiptService
from app.services.units import UnitService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_unit_service(db: Session = Depends(get_db)) -> UnitService:
    unit_repo = UnitRepository(Unit)
    return UnitService(unit_repo, db)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    product_repo = ProductRepository(Product)
    unit_repo = UnitRepository(Unit)
    return ProductService(product_repo, unit_repo, db)


def get_receipt_service(db: Session = Depends(get_db)) -> ReceiptService:
    receipt_repo = ReceiptRepository(Receipt)
    product_repo = ProductRepository(Product)
    return ReceiptService(receipt_repo, product_repo, db)
