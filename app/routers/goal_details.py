from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/goal_details", tags=["goal_details"])

@router.post("/", response_model=schemas.GoalDetail)
def create_goal_detail(gd: schemas.GoalDetailCreate, db: Session = Depends(get_db)):
    return crud.create_goal_detail(db, gd)

@router.get("/", response_model=List[schemas.GoalDetail])
def read_goal_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goal_details(db, skip, limit)

@router.get("/{gd_id}", response_model=schemas.GoalDetail)
def read_goal_detail(gd_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_goal_detail(db, gd_id)
    if not db_obj:
        raise HTTPException(404, "GoalDetail not found")
    return db_obj
