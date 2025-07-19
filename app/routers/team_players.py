from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/team_players", tags=["team_players"])

@router.post("/", response_model=schemas.TeamPlayer)
def create_team_player(tp: schemas.TeamPlayerCreate, db: Session = Depends(get_db)):
    return crud.create_team_player(db, tp)

@router.get("/", response_model=List[schemas.TeamPlayer])
def read_team_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_team_players(db, skip, limit)

@router.get("/{tp_id}", response_model=schemas.TeamPlayer)
def read_team_player(tp_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_team_player(db, tp_id)
    if not db_obj:
        raise HTTPException(404, "TeamPlayer not found")
    return db_obj
