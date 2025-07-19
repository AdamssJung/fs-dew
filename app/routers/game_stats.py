from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/game_stats", tags=["game_stats"])

@router.post("/", response_model=schemas.GameStat)
def create_game_stat(gs: schemas.GameStatCreate, db: Session = Depends(get_db)):
    return crud.create_game_stat(db, gs)

@router.get("/", response_model=List[schemas.GameStat])
def read_game_stats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_game_stats(db, skip, limit)

@router.get("/{gs_id}", response_model=schemas.GameStat)
def read_game_stat(gs_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_game_stat(db, gs_id)
    if not db_obj:
        raise HTTPException(404, "GameStat not found")
    return db_obj
