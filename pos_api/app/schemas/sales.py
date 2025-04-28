from pydantic import BaseModel


class SalesReport(BaseModel):
    n_receipts: int
    revenue: int


class SalesReportResponse(BaseModel):
    sales: SalesReport
