"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy.orm import Session
from app.category.category_model import Category
from app.category.category_schema import CategoryBase, CategoryUpdate
from app.user.user_model import User
from app.category import category_db
from app.bill import bill_db
from app.core.errors import ForbiddenError, ResourceNotFoundError, AlreadyExistsError, DeleteConflictError

# Create a new category
def create_category(db: Session, current_user: User, category: CategoryBase) -> Category:
    # Check name unicity
    existing_cat = category_db.get_category_by_name(db, current_user.id, category.name)
    if existing_cat:
        raise AlreadyExistsError(message="Nom de catégorie déjà utilisé")
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
        raise ResourceNotFoundError(message=f"Catégorie {cat_id} inconnue")
    
    return category

# Get an existing category by its name - filtered by current user
def get_category_by_name(db: Session, current_user: User, name: str) -> Category:
    category = category_db.get_category_by_name(db, current_user.id, name)
    if not category:
        raise ResourceNotFoundError(message="Catégorie '{name}' inconnue")
    return category

# Update an existing category
def update_category(db: Session, current_user: User, cat_id: int, updates: CategoryUpdate) -> Category:
    category = get_category_by_id(db, current_user, cat_id)
    
    # Check if user can update this category
    if current_user.id != category.user_id:
        raise ForbiddenError(message="Vous ne pouvez pas modifier cette catégorie.")
    
    if updates.name:
        existing_cat = category_db.get_category_by_name(db, current_user.id, updates.name)
        if existing_cat and existing_cat.id != category.id:
            raise AlreadyExistsError(message="Il existe déjà une catégorie avec ce nom")
   
    update_data = updates.model_dump(exclude_unset=True)
     
    return category_db.update_category(db, category, update_data)

# Delete an existing category
def delete_category(db: Session, current_user: User, cat_id: int):
    category = get_category_by_id(db, current_user, cat_id)
    
    # Check if user can delete this category
    if current_user.id != category.user_id:
        raise ForbiddenError(message="Vous ne pouvez pas supprimer cette catégorie.")

    # Check if category is unused
    billsUsingCat = bill_db.get_all_bills(db, current_user.id, category_id=category.id)
    if any(billsUsingCat):
        raise DeleteConflictError(message="Cette catégorie est utilisée, vous ne pouvez la supprimer")

    return category_db.delete_category(db, category)

# Create a default category
def create_default(db: Session, current_user: User):
    cat = Category( name= "Autres", color= "#CCCCCC", user_id = current_user.id )
    return category_db.create_category(db, cat)