from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.crud import user_db
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.models.user import User

# Create a new user
def create_user(db: Session, user: UserCreate) -> User:
    # Check email unicity
    existing_user = user_db.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Email déjà utilisé")
    
    # Password hash before creating
    hashed_password = hash_password(user.password)
    # User db model to create
    user_to_create = User(
        **user.model_dump(exclude={'password'}),
        password_hash = hashed_password
    )

    return user_db.create_user(db, user_to_create)

# Get all users
def get_all_users(db: Session) -> list[User]:
    return user_db.get_all_users(db)

# Find a user by its id
def get_user_by_id(db: Session, user_id: int) -> User:
    user = user_db.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    return user

# Find a user by its email
def get_user_by_email(db: Session, email: str) -> User:
    user = user_db.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    return user

# Update the logged user
def update_user(db: Session, current_user: User, updates: UserUpdate, user_email: str) -> User:
    if not current_user :
        raise HTTPException(status_code=401, detail=f"Il faut être connecté pour pouvoir exécuter cette opération")
    
    # Current user (db model)
    user = user_db.get_user_by_email(db, user_email)  
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    
    # Verify if the user can update
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Vous ne pouvez pas modifier cet utilisateur.")
    
    # Generate update datas
    update_data = updates.model_dump(exclude_unset=True, exclude={'password'})
    if updates.password:
        update_data['password'] = hash_password(updates.password)

    return user_db.update_user(db, user, update_data)

# Delete an account
def delete_user(db: Session, current_user: User, user_email):
    if not current_user:
        raise HTTPException(status_code=401, detail=f"Il faut être connecté pour pouvoir exécuter cette opération")
    
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur inconnu")
    
     # Verify if the user can update
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Vous ne pouvez pas supprimer cet utilisateur.")
    
    return user_db.delete_user(db, user)