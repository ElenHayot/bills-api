from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

DEV_USER_EMAIL = "dev@example.com"
DEV_PASSWORD = "dev123PWD"

def seed_users(db: Session) -> User:
    user = db.query(User).filter_by(email=DEV_USER_EMAIL).first()
    if user:
        print("👤 User already exists")
        return user

    user = User(
        email=DEV_USER_EMAIL,
        password_hash=hash_password(DEV_PASSWORD)
    )
    db.add(user)
    db.flush()  # pour récupérer user.id

    print("👤 User created")
    return user