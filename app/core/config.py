from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Isul Futsal"
    API_V1_STR: str = "/api/v1"
    
    # DB 설정
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "db_fs")
    DB_USER: str = os.getenv("DB_USER", "app_fs")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "pok1234")

    # CORS 설정 (프론트엔드 도메인 추가 가능)
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]

settings = Settings()
