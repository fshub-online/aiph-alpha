from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from app.models.key_result import KeyResult
from app.schemas.key_result import KeyResultCreate, KeyResultUpdate

def get_key_result(db: Session, key_result_id: int) -> Optional[KeyResult]:
    return db.query(KeyResult).filter(KeyResult.id == key_result_id).first()

def get_key_results(db: Session, skip: int = 0, limit: int = 100) -> List[KeyResult]:
    return db.query(KeyResult).offset(skip).limit(limit).all()

def create_key_result(db: Session, *, obj_in: KeyResultCreate) -> KeyResult:
    db_obj = KeyResult(
        title=obj_in.title,
        description=obj_in.description,
        target_value=obj_in.target_value,
        current_value=obj_in.current_value,
        start_value=obj_in.start_value,
        unit=obj_in.unit,
        status=obj_in.status,
        complexity_level=obj_in.complexity_level,
        due_date=obj_in.due_date,
        objective_id=str(obj_in.objective_id),
        team_member_id=str(obj_in.team_member_id) if obj_in.team_member_id else None,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_key_result(db: Session, *, db_obj: KeyResult, obj_in: Union[KeyResultUpdate, Dict[str, Any]]) -> KeyResult:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_key_result(db: Session, *, key_result_id: int) -> Optional[KeyResult]:
    obj = db.query(KeyResult).get(key_result_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj

def get_key_results_by_objective(db: Session, objective_id: int):
    return db.query(KeyResult).filter(KeyResult.objective_id == objective_id).all()

