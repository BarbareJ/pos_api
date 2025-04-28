from sqlalchemy.orm import Session

from app.repositories.sales import SalesRepository


class SalesService:
    def __init__(self, repo: SalesRepository):
        self.repo = repo

    def get_sales_report(self, db: Session) -> tuple[int, int]:
        return self.repo.get_sales_report(db)
