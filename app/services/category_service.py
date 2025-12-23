from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.schemas.category import CategoryBase, CategoryUpdate
from app.models.user import User
from app.crud import category_db

# Create a new category
def create_category(db: Session, current_user: User, category: CategoryBase) -> Category:
    # Check name unicity
    existing_cat = category_db.get_category_by_name(db, current_user.id, category.name)
    if existing_cat:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Nom de catégorie déjà utilisé")
    category_to_create = Category(
        **category.model_dump(),
        user_id = current_user.id
    )
    return category_db.create_category(db, category_to_create)

# Get all categories - filtered by current user
def get_all_categories(db: Session, current_user: User) -> list[Category]:
    return category_db.get_all_categories(db, current_user.id)

# Get one category by its id - filtered by current user
def get_category_by_id(db: Session, current_user: User, cat_id: int) -> Category:
    category = category_db.get_category_by_id(db, current_user.id, cat_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catégorie {cat_id} inconnue")
    
    return category

# Get an existing category by its name - filtered by current user
def get_category_by_name(db: Session, current_user: User, name: str) -> Category:
    category = category_db.get_category_by_name(db, current_user.id, name)
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie inconnue")
    return category

# Update an existing category
def update_category(db: Session, current_user: User, name: str, updates: CategoryUpdate) -> Category:
    category = get_category_by_name(db, current_user, name)
    
    # Check if user can update this category
    if current_user.id != category.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas modifier cette catégorie.")
    
    update_data = updates.model_dump(exclude_unset=True)
    return category_db.update_category(db, category, update_data)

# Delete an existing category
def delete_category(db: Session, current_user: User, name: str):
    category = get_category_by_name(db, current_user, name)
    
    # Check if user can delete this category
    if current_user.id != category.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas supprimer cette catégorie.")

    return category_db.delete_category(db, category)

# Create a default category
def create_default(db: Session, current_user: User):
    cat = Category( name= "Autres", color= "#CCCCCC", user_id = current_user.id )
    return category_db.create_category(db, cat)