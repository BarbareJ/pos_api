from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Receipt, ReceiptStatus
from app.repositories.products import ProductRepository
from app.repositories.receipts import ReceiptRepository
from app.schemas.receipts import (
    ReceiptAddProductRequest,
    ReceiptCloseRequest,
    ReceiptItemResponse,
    ReceiptResponse,
)


class ReceiptService:
    def __init__(
        self,
        receipt_repo: ReceiptRepository,
        product_repo: ProductRepository,
        db: Session,
    ):
        self.receipt_repo = receipt_repo
        self.product_repo = product_repo
        self.db = db

    def build_receipt_response(self, receipt: Receipt) -> ReceiptResponse:
        return ReceiptResponse(
            id=str(receipt.id),
            status=receipt.status.value,
            total=int(receipt.total),
            products=[
                ReceiptItemResponse(
                    id=item.product_id,
                    quantity=item.quantity,
                    price=item.price_at_sale,
                    total=item.total_price,
                )
                for item in receipt.products
            ],
        )

    def create_receipt(self) -> ReceiptResponse:
        raw_receipt = self.receipt_repo.create(self.db, {})
        return self.build_receipt_response(raw_receipt)

    def get_receipt(self, receipt_id: str) -> Receipt:
        receipt = self.receipt_repo.get(self.db, receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Receipt with id<{receipt_id}> does not exist."},
            )
        return receipt

    def add_product(
        self, receipt_id: str, data: ReceiptAddProductRequest
    ) -> ReceiptResponse:
        receipt = self.get_receipt(receipt_id)
        if receipt.status == ReceiptStatus.CLOSED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": f"Cannot add product to closed receipt <{receipt_id}>."
                },
            )
        product = self.product_repo.get(self.db, data.id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail={"message": f"Product with id<{data.id}> does not exist."},
            )
        updated_receipt = self.receipt_repo.add_product(
            self.db, receipt, product, data.quantity
        )
        return self.build_receipt_response(updated_receipt)

    def close_receipt(
        self, receipt_id: str, req: ReceiptCloseRequest
    ) -> ReceiptResponse:
        receipt = self.get_receipt(receipt_id)
        if req.status == ReceiptStatus.CLOSED:
            self.receipt_repo.close_receipt(self.db, receipt)

        updated = self.get_receipt(receipt_id)
        return self.build_receipt_response(updated)

    def delete_receipt(self, receipt_id: str) -> None:
        receipt = self.get_receipt(receipt_id)
        if receipt.status == ReceiptStatus.CLOSED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": f"Receipt with id<{receipt_id}> is closed."},
            )
        self.receipt_repo.delete_receipt(self.db, receipt)
