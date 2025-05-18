from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app import schemas, crud
from app.db.session import get_db

router = APIRouter()

@router.get("/key_results/", response_model=List[schemas.key_result.KeyResult])
def read_key_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_key_result.crud_key_result.get_multi(db, skip=skip, limit=limit)

@router.post("/key_results/", response_model=schemas.key_result.KeyResult)
def create_key_result(key_result_in: schemas.key_result.KeyResultCreate, db: Session = Depends(get_db)):
    return crud.crud_key_result.crud_key_result.create(db, obj_in=key_result_in)

@router.get("/key_results/{id}", response_model=schemas.key_result.KeyResult)
def read_key_result(id: UUID, db: Session = Depends(get_db)):
    db_obj = crud.crud_key_result.crud_key_result.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="KeyResult not found")
    return db_obj

@router.put("/key_results/{id}", response_model=schemas.key_result.KeyResult)
def update_key_result(id: UUID, key_result_in: schemas.key_result.KeyResultUpdate, db: Session = Depends(get_db)):
    db_obj = crud.crud_key_result.crud_key_result.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="KeyResult not found")
    return crud.crud_key_result.crud_key_result.update(db, db_obj=db_obj, obj_in=key_result_in)

@router.delete("/key_results/{id}", response_model=schemas.key_result.KeyResult)
def delete_key_result(id: UUID, db: Session = Depends(get_db)):
    db_obj = crud.crud_key_result.crud_key_result.remove(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="KeyResult not found")
    return db_obj
