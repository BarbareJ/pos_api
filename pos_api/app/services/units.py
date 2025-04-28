from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Unit
from app.repositories.units import UnitRepository
from app.schemas.units import UnitCreate


class UnitService:

    def __init__(self, repo: UnitRepository, db: Session):
        self.repo = repo
        self.db = db

    def create_unit(self, data: UnitCreate) -> Unit:
        existing = self.repo.get_by_name(self.db, data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": f"Unit with name<{data.name}> already exists."},
            )
        return self.repo.create(self.db, {"name": data.name})

    def list_units(self) -> list[Unit]:
        return self.repo.list_all(self.db)

    def get_unit(self, unit_id: str) -> Unit:
        unit = self.repo.get(self.db, unit_id)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Unit with id<{unit_id}> does not exist."},
            )
        return unit
