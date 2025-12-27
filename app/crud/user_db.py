from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.user import User
from app.core.security import verify_password
from typing import Optional

# Get all users
def get_all_users(db: Session) -> list[User]:
    users = db.execute(select(User).order_by(User.email.asc()))
    return users.scalars().all()

# Find a user by its id
def get_user_by_id(db: Session, user_id: int) -> User | None:
    query = select(User).filter(User.id == user_id)
    user = db.execute(query)
    return user.scalar_one_or_none()

# Find a user by its email
def get_user_by_email(db: Session, email: str) -> User | None:
    query = select(User).filter(User.email == email)
    user = db.execute(query)
    return user.scalar_one_or_none()

# Add a new user in db
def create_user(db: Session, db_user: User) -> User:
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update an existing user in db
def update_user(db: Session, user: User, updates: dict) -> User:
    for key, value in updates.items():
        # Rename the key "password" to "password_hash" for db_user
        if key == "password" : key = "password_hash"
        if hasattr(user, key):  # petit garde-fou si mauvaise key
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# Remove a user from db
def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

"""
# Authenticate a user with its {email, password}
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user
"""