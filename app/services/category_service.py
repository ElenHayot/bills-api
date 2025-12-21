from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.schemas.category import CategoryBase, CategoryUpdate
from app.models.user import User
from app.crud import category_db

# Create a new category
def create_category(db: Session, category: CategoryBase, current_user: User) -> Category:
    # Check name unicity
    existing_cat = category_db.get_category_by_name(db, category.name)
    if existing_cat:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Nom de catégorie déjà utilisé")
    category_to_create = Category(
        **category.model_dump(),
        user_id = current_user.id
    )
    return category_db.create_category(db, category_to_create)

# Get all categories
def get_all_categories(db: Session, user_id: int = None) -> list[Category]:
    return category_db.get_all_categories(db, user_id)

# Get an existing category by its name
def get_category_by_name(db: Session, name: str) -> Category:
    category = category_db.get_category_by_name(db, name)
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie inconnue")
    return category

# Update an existing category
def update_category(db: Session, name: str, updates: CategoryUpdate, current_user: User) -> Category:
    category = category_db.get_category_by_name(db, name)
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie inconnue")
    
    # Check if user can update this category
    if current_user.id != category.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas modifier cette catégorie.")
    
    update_data = updates.model_dump(exclude_unset=True)
    return category_db.update_category(db, category, update_data)

# Delete an existing category
def delete_category(db: Session, name: str, current_user: User):
    category = category_db.get_category_by_name(db, name)
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie inconnue")
    
    # Check if user can delete this category
    if current_user.id != category.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas supprimer cette catégorie.")

    return category_db.delete_category(category)