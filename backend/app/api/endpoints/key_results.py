from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union, Dict, Any
from app import schemas, crud
from app.db.session import get_db
from app.models.key_result import KeyResultStatus, KeyResultComplexityLevel

router = APIRouter()


@router.get("/", response_model=List[schemas.key_result.KeyResult])
def read_key_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_key_result.get_key_results(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.key_result.KeyResult)
def create_key_result(
    key_result_in: schemas.key_result.KeyResultCreate, db: Session = Depends(get_db)
):
    return crud.crud_key_result.create_key_result(db, obj_in=key_result_in)


@router.get("/enums", tags=["key_results"])
def get_key_result_enums():
    return {
        "status": [status.value for status in KeyResultStatus],
        "complexity_level": [level.value for level in KeyResultComplexityLevel],
    }


@router.get("/{key_result_id}", response_model=schemas.key_result.KeyResult)
def read_key_result(key_result_id: int, db: Session = Depends(get_db)):
    db_obj = crud.crud_key_result.get_key_result(db, key_result_id=key_result_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="KeyResult not found")
    return db_obj


@router.put("/{key_result_id}", response_model=schemas.key_result.KeyResult)
def update_key_result(
    key_result_id: int,
    key_result_in: Union[schemas.key_result.KeyResultUpdate, Dict[str, Any]],
    db: Session = Depends(get_db),
):
    db_obj = crud.crud_key_result.get_key_result(db, key_result_id=key_result_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="KeyResult not found")
    return crud.crud_key_result.update_key_result(
        db, db_obj=db_obj, obj_in=key_result_in
    )


@router.delete("/{key_result_id}", response_model=schemas.key_result.KeyResult)
def delete_key_result(key_result_id: int, db: Session = Depends(get_db)):
    db_obj = crud.crud_key_result.delete_key_result(db, key_result_id=key_result_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="KeyResult not found")
    return db_obj
