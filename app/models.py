# app/models.py
from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean,
    ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    backno = Column(Integer)
    profile_image_url = Column(Text)
    status = Column(String(50), default="active")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    # relationships
    goal_scored = relationship("GoalDetail", back_populates="scorer", foreign_keys="GoalDetail.scorer_id")
    goal_assisted = relationship("GoalDetail", back_populates="assist", foreign_keys="GoalDetail.assist_id")
    votes = relationship("MomVote", back_populates="player")

class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    season_name = Column(String(100), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    matches = relationship("Match", back_populates="season")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    match_date = Column(Date, nullable=False)
    total_teams = Column(Integer)
    location = Column(String(100))
    season_id = Column(Integer, ForeignKey("seasons.id"))
    status = Column(String(50), default="scheduled")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    season = relationship("Season", back_populates="matches")
    teams = relationship("Team", back_populates="match")
    votes = relationship("MomVote", back_populates="match")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"))
    team_name = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    match = relationship("Match", back_populates="teams")
    players = relationship("TeamPlayer", back_populates="team")
    stats = relationship("GameStat", back_populates="team")

class TeamPlayer(Base):
    __tablename__ = "team_players"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    team = relationship("Team", back_populates="players")
    player = relationship("Player")

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"))
    gameno = Column(Integer)
    home_team_name = Column(String(50))
    home_score = Column(Integer)
    home_keeper = Column(String(100))
    away_team_name = Column(String(50))
    away_score = Column(Integer)
    away_keeper = Column(String(100))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    stats = relationship("GameStat", back_populates="game")
    goals = relationship("GoalDetail", back_populates="game")

class MomVote(Base):
    __tablename__ = "mom_votes"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"))
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))
    vote_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    match = relationship("Match", back_populates="votes")
    player = relationship("Player", back_populates="votes")

class GameStat(Base):
    __tablename__ = "game_stats"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    score = Column(Integer)
    goals_conceded = Column(Integer)
    keeper_goals_conceded = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    game = relationship("Game", back_populates="stats")
    team = relationship("Team", back_populates="stats")

class GoalDetail(Base):
    __tablename__ = "goal_details"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"))
    scorer_id = Column(Integer, ForeignKey("players.id"))
    assist_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    own_goal = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    game = relationship("Game", back_populates="goals")
    scorer = relationship("Player", back_populates="goal_scored", foreign_keys=[scorer_id])
    assist = relationship("Player", back_populates="goal_assisted", foreign_keys=[assist_id])
    team = relationship("Team")
