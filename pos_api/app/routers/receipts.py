from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.dependencies import get_receipt_service
from app.schemas.receipts import (
    ReceiptAddProductRequest,
    ReceiptCloseRequest,
    ReceiptCreate,
    ReceiptCreateResponse,
    ReceiptReadResponse,
)
from app.services.receipts import ReceiptService

router = APIRouter()

@router.post("", response_model=ReceiptCreateResponse, status_code=201)
def create_receipt(
    _: ReceiptCreate,
    service: ReceiptService = Depends(get_receipt_service)
) -> Dict[str, Any]:
    receipt = service.create_receipt()
    return {"receipt": receipt}

@router.post("/{receipt_id}/products", response_model=ReceiptReadResponse, status_code=201)
def add_product_to_receipt(
    receipt_id: str,
    data: ReceiptAddProductRequest,
    service: ReceiptService = Depends(get_receipt_service)
) -> Dict[str, Any]:
    updated_receipt = service.add_product(receipt_id, data)
    return {"receipt": updated_receipt}

@router.get("/{receipt_id}", response_model=ReceiptReadResponse, status_code=200)
def read_receipt(
    receipt_id: str,
    service: ReceiptService = Depends(get_receipt_service)
) -> Dict[str, Any]:
    receipt = service.get_receipt(receipt_id)
    return {"receipt": receipt}

@router.patch("/{receipt_id}", response_model=ReceiptReadResponse, status_code=200)
def close_receipt(
    receipt_id: str,
    req: ReceiptCloseRequest,
    service: ReceiptService = Depends(get_receipt_service)
) -> Dict[str, Any]:
    updated = service.close_receipt(receipt_id, req)
    return {"receipt": updated}

@router.delete("/{receipt_id}", status_code=200)
def delete_receipt(
    receipt_id: str,
    service: ReceiptService = Depends(get_receipt_service)
) -> Dict[str, Any]:
    service.delete_receipt(receipt_id)
    return {}

