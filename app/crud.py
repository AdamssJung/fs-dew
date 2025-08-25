# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, security
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

# ─────────────────────────────────────────────────────────────
# Player
# ─────────────────────────────────────────────────────────────
def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def create_player(db: Session, player: schemas.PlayerCreate):
    db_obj = models.Player(**player.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# Season
# ─────────────────────────────────────────────────────────────
def get_season(db: Session, season_id: int):
    return db.query(models.Season).filter(models.Season.id == season_id).first()

def get_seasons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Season).offset(skip).limit(limit).all()

def create_season(db: Session, season: schemas.SeasonCreate):
    db_obj = models.Season(**season.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# Match
# ─────────────────────────────────────────────────────────────
def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()

def create_match(db: Session, match: schemas.MatchCreate):
    db_obj = models.Match(**match.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# Team
# ─────────────────────────────────────────────────────────────
def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate):
    db_obj = models.Team(**team.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# TeamPlayer
# ─────────────────────────────────────────────────────────────
def get_team_player(db: Session, tp_id: int):
    return db.query(models.TeamPlayer).filter(models.TeamPlayer.id == tp_id).first()

def get_team_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TeamPlayer).offset(skip).limit(limit).all()

def create_team_player(db: Session, tp: schemas.TeamPlayerCreate):
    db_obj = models.TeamPlayer(**tp.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# Game
# ─────────────────────────────────────────────────────────────
def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()

def create_game(db: Session, game: schemas.GameCreate):
    db_obj = models.Game(**game.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# MomVote
# ─────────────────────────────────────────────────────────────
def get_mom_vote(db: Session, mv_id: int):
    return db.query(models.MomVote).filter(models.MomVote.id == mv_id).first()

def get_mom_votes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MomVote).offset(skip).limit(limit).all()

def create_mom_vote(db: Session, mv: schemas.MomVoteCreate):
    db_obj = models.MomVote(**mv.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# GameStat
# ─────────────────────────────────────────────────────────────
def get_game_stat(db: Session, gs_id: int):
    return db.query(models.GameStat).filter(models.GameStat.id == gs_id).first()

def get_game_stats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GameStat).offset(skip).limit(limit).all()

def create_game_stat(db: Session, gs: schemas.GameStatCreate):
    db_obj = models.GameStat(**gs.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# GoalDetail
# ─────────────────────────────────────────────────────────────
def get_goal_detail(db: Session, gd_id: int):
    return db.query(models.GoalDetail).filter(models.GoalDetail.id == gd_id).first()

def get_goal_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GoalDetail).offset(skip).limit(limit).all()

def create_goal_detail(db: Session, gd: schemas.GoalDetailCreate):
    db_obj = models.GoalDetail(**gd.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

# ───────────────────────────────
# GameGuest (용병)
# ───────────────────────────────
def get_game_guest(db: Session, guest_id: int):
    return db.query(models.GameGuest).filter(models.GameGuest.id == guest_id).first()

def get_game_guests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GameGuest).offset(skip).limit(limit).all()

def create_game_guest(db: Session, game_guest: schemas.GameGuestCreate):
    db_obj = models.GameGuest(**game_guest.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# ─────────────────────────────────────────────────────────────
# Get User
# ─────────────────────────────────────────────────────────────
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# ─────────────────────────────────────────────────────────────
# Create User
# ─────────────────────────────────────────────────────────────
def create_player(db: Session, player: schemas.PlayerCreate):
    db_obj = models.Player(**player.dict())
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        db.rollback()
        # 중복 키나 유니크 제약 실패 등을 400/409로 예쁘게 내려줄 수도 있어요
        raise HTTPException(status_code=409, detail="Player insert failed: duplicate or constraint violation")
