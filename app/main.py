# app/main.py
from fastapi import FastAPI
from .routers import (
    players, seasons, matches, teams, team_players,
    games, mom_votes, game_stats, goal_details, auth
)

app = FastAPI(title="이슬처럼 풋살 API")

# include all routers
app.include_router(players.router)
app.include_router(seasons.router)
app.include_router(matches.router)
app.include_router(teams.router)
app.include_router(team_players.router)
app.include_router(games.router)
app.include_router(mom_votes.router)
app.include_router(game_stats.router)
app.include_router(goal_details.router)
app.include_router(auth.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
