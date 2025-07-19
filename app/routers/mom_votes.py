from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/mom_votes", tags=["mom_votes"])

@router.post("/", response_model=schemas.MomVote)
def create_mom_vote(mv: schemas.MomVoteCreate, db: Session = Depends(get_db)):
    return crud.create_mom_vote(db, mv)

@router.get("/", response_model=List[schemas.MomVote])
def read_mom_votes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_mom_votes(db, skip, limit)

@router.get("/{mv_id}", response_model=schemas.MomVote)
def read_mom_vote(mv_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_mom_vote(db, mv_id)
    if not db_obj:
        raise HTTPException(404, "MomVote not found")
    return db_obj
