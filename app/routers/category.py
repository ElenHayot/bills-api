from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.category import CategoryBase, CategoryRead, CategoryUpdate
from app.dependencies.auth import get_current_user
from app.services import category_service

category_router = APIRouter(tags=["Categories"])

# POST : Create a category for the current user
@category_router.post("/", response_model=CategoryRead)
def create(cat_data: CategoryBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.create_category(db, current_user, cat_data)

# GET : get all current user's categories
@category_router.get("/", response_model=list[CategoryRead])
def read_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.get_all_categories(db, current_user)

# GET : Get one category by its name, filtered by current user
@category_router.get("/{cat_name}", response_model=CategoryRead)
def read(cat_name: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.get_category_by_name(db, current_user, cat_name)

# PUT : Update a current user's category
@category_router.put("/{cat_name}", response_model=CategoryRead)
def update(cat_name: str, updates: CategoryUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.update_category(db, current_user, cat_name, updates)

# DELETE : Delete a category from the current user
@category_router.delete("/{cat_name}")
def delete(cat_name: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.delete_category(db, current_user, cat_name)