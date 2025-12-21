from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.category import CategoryBase, CategoryRead, CategoryUpdate
from app.dependencies.auth import get_current_user
from app.services import category_service

category_router = APIRouter(tags=["Categories"])

# POST : Create a category
@category_router.post("/", response_model=CategoryRead)
def create(cat_data: CategoryBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.create_category(db, cat_data, current_user)

# GET : get all categories
@category_router.get("/", response_model=list[CategoryRead])
def read_all(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)

# GET : Get one category
@category_router.get("/{cat_name}", response_model=CategoryRead)
def read(db: Session, cat_name: str):
    return category_service.get_category_by_name(db, cat_name)

# PUT : Update a category
@category_router.put("/{cat_name}", response_model=CategoryRead)
def update(cat_name: str, updates: CategoryUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.update_category(db, cat_name, updates, current_user)

# DELETE : Delete a category
@category_router.delete("/{cat_name}")
def delete(cat_name: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.delete_category(db, cat_name)