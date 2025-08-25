# app/routers/game_guests.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/game_guests", tags=["game_guests"])

@router.post("/", response_model=schemas.GameGuest)
def create_game_guest(
    guest: schemas.GameGuestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)   # JWT 인증 필요
):
    return crud.create_game_guest(db, guest)

@router.get("/", response_model=List[schemas.GameGuest])
def read_game_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_game_guests(db, skip, limit)

@router.get("/{guest_id}", response_model=schemas.GameGuest)
def read_game_guest(guest_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_game_guest(db, guest_id)
    if not db_obj:
        raise HTTPException(404, "GameGuest not found")
    return db_obj
