from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import crud, schemas
from ..dependencies import get_current_user, get_db

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_player(db, player)

@router.get("/", response_model=List[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_players(db, skip, limit)

@router.get("/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_player(db, player_id)
    if not db_obj:
        raise HTTPException(404, "Player not found")
    return db_obj
