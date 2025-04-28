from sqlalchemy.orm import Session

from app.models import Product, Receipt, ReceiptItem
from app.repositories.base import BaseRepository


class ReceiptRepository(BaseRepository[Receipt]):
    def add_product(
            self,
            db: Session,
            receipt: Receipt,
            product: Product,
            quantity: int
    ) -> Receipt:
        price_at_sale = product.price
        total_price = price_at_sale * quantity
        item = ReceiptItem(
            receipt_id=receipt.id,
            product_id=product.id,
            quantity=quantity,
            price_at_sale=price_at_sale,
            total_price=total_price,
        )
        db.add(item)
        receipt.total = receipt.total + (product.price * quantity)
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt

    def close_receipt(self, db: Session, receipt: Receipt) -> None:
        receipt.status = "closed"
        db.add(receipt)
        db.commit()
        db.refresh(receipt)

    def delete_receipt(self, db: Session, receipt: Receipt) -> None:
        db.delete(receipt)
        db.commit()
