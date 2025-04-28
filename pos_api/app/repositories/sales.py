from sqlalchemy.orm import Session

from app.models import Receipt, ReceiptStatus


class SalesRepository:
    def get_sales_report(self, db: Session) -> tuple[int, int]:
        closed_receipts = db.query(Receipt).filter(Receipt.status == ReceiptStatus.CLOSED).all()

        total_revenue = sum(receipt.total for receipt in closed_receipts)

        n_receipts = len(closed_receipts)

        return n_receipts, total_revenue
