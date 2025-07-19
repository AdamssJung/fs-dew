from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/seasons", tags=["seasons"])

@router.post("/", response_model=schemas.Season)
def create_season(season: schemas.SeasonCreate, db: Session = Depends(get_db)):
    return crud.create_season(db, season)

@router.get("/", response_model=List[schemas.Season])
def read_seasons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_seasons(db, skip, limit)

@router.get("/{season_id}", response_model=schemas.Season)
def read_season(season_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_season(db, season_id)
    if not db_obj:
        raise HTTPException(404, "Season not found")
    return db_obj
