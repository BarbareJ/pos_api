from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories.sales import SalesRepository
from app.schemas.sales import SalesReportResponse
from app.services.sales import SalesService

router = APIRouter()


@router.get("", response_model=SalesReportResponse, status_code=200)
def get_sales_report(db: Session = Depends(get_db)):
    service = SalesService(SalesRepository())
    n_receipts, revenue = service.get_sales_report(db)
    return {"sales": {"n_receipts": n_receipts, "revenue": revenue}}
