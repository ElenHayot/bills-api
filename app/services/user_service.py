from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.crud import user_db
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password
from app.models.user import User

# Create a new user
def create_user(db: Session, user: UserCreate):
    # Check email unicity
    existing_user = user_db.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail="Email déjà utilisé"
            )
    
    # Password hash before creating
    hashed_password = hash_password(user.password)
    # User db model to create
    user = User(
        **user.model_dump(exclude={'password'}),
        password_hash = hashed_password
    )

    return user_db.create_user(db, user)

# Find a user by its id
def get_user_by_id(db: Session, user_id: int):
    user = user_db.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    return user

# Find a user by its email
def get_user_by_email(db: Session, email: str):
    user = user_db.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    return user

# Update the logged user
def update_user(db: Session, logged_user, updates: UserCreate):   
    # Current user (db model)
    user= user_db.get_user_by_id(db, logged_user.id)  
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")

    # Generate update datas
    update_data = updates.model_dump(exclude_unset=True, exclude={'password'})
    if updates.password:
        update_data['password'] = hash_password(updates.password)

    return user_db.update_user(db, user, update_data)

# Delete an account
def delete_user(db: Session, logged_user):
    # Current user (db model)
    user = user_db.get_user_by_id(db, logged_user.id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    
    return user_db.delete_user(db, user)