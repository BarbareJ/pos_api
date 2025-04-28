from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Product
from app.repositories.products import ProductRepository
from app.repositories.units import UnitRepository
from app.schemas.products import ProductCreate, ProductUpdate


class ProductService:
    def __init__(
        self, product_repo: ProductRepository, unit_repo: UnitRepository, db: Session
    ):
        self.product_repo = product_repo
        self.unit_repo = unit_repo
        self.db = db

    def create_product(self, data: ProductCreate) -> Product:
        existing = self.product_repo.get_by_barcode(self.db, data.barcode)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": f"Product with barcode<{data.barcode}> already exists."
                },
            )
        return self.product_repo.create(self.db, data.dict())

    def list_products(self) -> list[Product]:
        return self.product_repo.list_all(self.db)

    def get_product(self, product_id: str) -> Product:
        product = self.product_repo.get(self.db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Product with id<{product_id}> does not exist."},
            )
        return product

    def update_product(self, product_id: str, data: ProductUpdate) -> None:
        product = self.get_product(product_id)
        self.product_repo.update_price(self.db, product, int(data.price))
