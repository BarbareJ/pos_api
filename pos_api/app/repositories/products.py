from sqlalchemy.orm import Session

from app.models import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def get_by_barcode(self, db: Session, barcode: str) -> Product | None:
        return db.query(Product).filter(Product.barcode == barcode).first()

    def update_price(self, db: Session, product: Product, new_price: int) -> None:
        product.price = new_price
        db.add(product)
        db.commit()
        db.refresh(product)
