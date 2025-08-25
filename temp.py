from app.database import SessionLocal
from app import crud

db = SessionLocal()
user = crud.get_user_by_username(db, "testuser")
print(user)

from app.security import verify_password

print("username:", user.username)
print("hashed_password:", user.hashed_password)
print("verify:", verify_password("testpass", user.hashed_password))


from app.security import get_password_hash, verify_password

# 새로 해시 생성
hashed = get_password_hash("testpass")
print("new hash:", hashed)

# 이 새 해시로 검증 → True
print("verify:", verify_password("testpass", hashed))


from app.database import SessionLocal
from app import crud, schemas

db = SessionLocal()
user = crud.create_user(db, schemas.UserCreate(username="testuser2", password="testpass"))
print(user.username, user.hashed_password)

