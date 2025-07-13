from fastapi import APIRouter, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from db.session import get_db_connection

router = APIRouter()

@router.get("/")
def get_players():
    """전체 선수 목록 조회 API"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, backno FROM tb_players;") # DB에서 선수 목록 가져오기
        players = cur.fetchall()
        conn.close()
        return {"players": players}
    except Exception as e:
        return {"error": str(e)}
