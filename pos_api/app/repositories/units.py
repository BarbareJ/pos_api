from sqlalchemy.orm import Session

from app.models import Unit
from app.repositories.base import BaseRepository


class UnitRepository(BaseRepository[Unit]):
    def get_by_name(self, db: Session, name: str) -> Unit | None:
        return db.query(Unit).filter(Unit.name == name).first()
