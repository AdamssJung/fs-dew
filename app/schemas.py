# app/schemas.py
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# ─────────────────────────────────────────────────────────────
# Player
# ─────────────────────────────────────────────────────────────
class PlayerBase(BaseModel):
    name: str
    email: Optional[str] = None
    backno: Optional[int] = None
    profile_image_url: Optional[str] = None
    status: Optional[str] = "active"

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# Season
# ─────────────────────────────────────────────────────────────
class SeasonBase(BaseModel):
    season_name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class SeasonCreate(SeasonBase):
    pass

class Season(SeasonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# Match
# ─────────────────────────────────────────────────────────────
class MatchBase(BaseModel):
    match_date: date
    total_teams: Optional[int] = None
    location: Optional[str] = None
    season_id: Optional[int] = None
    status: Optional[str] = "scheduled"

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# Team
# ─────────────────────────────────────────────────────────────
class TeamBase(BaseModel):
    match_id: int
    team_name: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# TeamPlayer
# ─────────────────────────────────────────────────────────────
class TeamPlayerBase(BaseModel):
    team_id: int
    player_id: int

class TeamPlayerCreate(TeamPlayerBase):
    pass

class TeamPlayer(TeamPlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# Game
# ─────────────────────────────────────────────────────────────
class GameBase(BaseModel):
    match_id: int
    gameno: Optional[int] = None
    home_team_name: Optional[str] = None
    home_score: Optional[int] = None
    home_keeper: Optional[str] = None
    away_team_name: Optional[str] = None
    away_score: Optional[int] = None
    away_keeper: Optional[str] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# MomVote
# ─────────────────────────────────────────────────────────────
class MomVoteBase(BaseModel):
    match_id: int
    player_id: int
    vote_count: Optional[int] = 0

class MomVoteCreate(MomVoteBase):
    pass

class MomVote(MomVoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# GameStat
# ─────────────────────────────────────────────────────────────
class GameStatBase(BaseModel):
    game_id: int
    team_id: int
    score: Optional[int] = None
    goals_conceded: Optional[int] = None
    keeper_goals_conceded: Optional[int] = None

class GameStatCreate(GameStatBase):
    pass

class GameStat(GameStatBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ─────────────────────────────────────────────────────────────
# GoalDetail
# ─────────────────────────────────────────────────────────────
class GoalDetailBase(BaseModel):
    game_id: int
    scorer_id: Optional[int] = None
    assist_id: Optional[int] = None
    team_id: Optional[int] = None
    own_goal: Optional[bool] = False

class GoalDetailCreate(GoalDetailBase):
    pass

class GoalDetail(GoalDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ─────────────────────────────────────────────────────────────
# 인증용 스키마
# ─────────────────────────────────────────────────────────────
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
