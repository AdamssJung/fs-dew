from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config.db_config import DATABASE_CONFIG

Base = declarative_base()

# Database Engine
def get_engine():
    db_url = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
             f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
    return create_engine(db_url)

# Seasons
class Season(Base):
    __tablename__ = 'tb_seasons'
    id = Column(Integer, primary_key=True, autoincrement=True)
    season_name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Matches
class Match(Base):
    __tablename__ = 'tb_matches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_date = Column(DateTime, nullable=False)
    season_id = Column(Integer, ForeignKey('tb_seasons.id'), nullable=False)
    total_teams = Column(Integer, nullable=False)
    location = Column(String(200))
    status = Column(String(50), default="scheduled")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    season = relationship("Season", back_populates="matches")

Season.matches = relationship("Match", order_by=Match.id, back_populates="season")

# Players
class Player(Base):
    __tablename__ = 'tb_players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    backNo = Column(Integer)
    profile_image_url = Column(Text)
    status = Column(String(50), default="active")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Team Players
class TeamPlayer(Base):
    __tablename__ = 'tb_team_players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('tb_matches.id'), nullable=False)
    team_name = Column(String(50), nullable=False)
    player_id = Column(Integer, ForeignKey('tb_players.id'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    match = relationship("Match", back_populates="team_players")
    player = relationship("Player", back_populates="team_players")

Match.team_players = relationship("TeamPlayer", order_by=TeamPlayer.id, back_populates="match")
Player.team_players = relationship("TeamPlayer", order_by=TeamPlayer.id, back_populates="player")

# Games
class Game(Base):
    __tablename__ = 'tb_games'
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('tb_matches.id'), nullable=False)
    gameno = Column(Integer, nullable=False)
    home_team_name = Column(String(50), nullable=False)
    home_score = Column(Integer, default=0)
    home_keeper = Column(Integer, ForeignKey('tb_players.id'))
    away_team_name = Column(String(50), nullable=False)
    away_score = Column(Integer, default=0)
    away_keeper = Column(Integer, ForeignKey('tb_players.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Goal Details
class GoalDetail(Base):
    __tablename__ = 'tb_goal_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('tb_games.id'), nullable=False)
    scorer_id = Column(Integer, ForeignKey('tb_players.id'), nullable=False)
    assist_id = Column(Integer, ForeignKey('tb_players.id'))
    team_name = Column(String(50), nullable=False)
    own_goal = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Sheet URLs
class SheetURL(Base):
    __tablename__ = 'tb_sheeturls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('tb_matches.id'), nullable=False)
    sheet_url = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# MOM Votes
class MomVote(Base):
    __tablename__ = 'tb_mom_votes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('tb_matches.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('tb_players.id'), nullable=False)
    vote_count = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Database initialization
def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=get_engine())
