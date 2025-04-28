from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, obj_id: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def list_all(self, db: Session) -> list[ModelType]:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: dict[str, Any]) -> ModelType:
        db_obj: ModelType = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
