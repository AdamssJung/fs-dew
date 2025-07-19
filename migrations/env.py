import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- .env 로드 ---
from dotenv import load_dotenv
load_dotenv()

# --- Base.metadata import ---
from app.models import Base

# Alembic Config 객체
config = context.config

# ini 파일의 [alembic] 섹션을 dict로 가져옵니다.
section = config.get_section(config.config_ini_section)

# .env의 DATABASE_URL로 덮어쓰기
section["sqlalchemy.url"] = os.getenv("DATABASE_URL")

# (선택) 디버그 출력
print(">>> OVERRIDDEN URL:", section["sqlalchemy.url"])

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# autogenerate 를 위한 metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """오프라인 모드: URL만으로 마이그레이션"""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # 섹션 가져오기 (ini 파일의 [alembic] 부분)
    section = config.get_section(config.config_ini_section)

    # 디버그: 실제 쓰는 URL 찍어보기
    print(">>> ALEMBIC USING URL:", section.get("sqlalchemy.url"))
    """온라인 모드: 실제 DB 연결 후 마이그레이션"""
    connectable = engine_from_config(
        # ★ 수정 포인트: 인자는 section 이름만!
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # compare_type=True  # 필요시 타입 변경도 감지
        )

        with context.begin_transaction():
            context.run_migrations()


# offline/online 분기
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
