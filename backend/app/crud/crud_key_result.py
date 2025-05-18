from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.key_result import KeyResult
from app.schemas.key_result import KeyResultCreate, KeyResultUpdate

class CRUDKeyResult:
    def get(self, db: Session, id: UUID) -> Optional[KeyResult]:
        return db.query(KeyResult).filter(KeyResult.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[KeyResult]:
        return db.query(KeyResult).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: KeyResultCreate) -> KeyResult:
        db_obj = KeyResult(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: KeyResult, obj_in: KeyResultUpdate) -> KeyResult:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: UUID) -> Optional[KeyResult]:
        obj = db.query(KeyResult).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

crud_key_result = CRUDKeyResult()
