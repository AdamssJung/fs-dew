from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db, match)

@router.get("/", response_model=List[schemas.Match])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_matches(db, skip, limit)

@router.get("/{match_id}", response_model=schemas.Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_match(db, match_id)
    if not db_obj:
        raise HTTPException(404, "Match not found")
    return db_obj
