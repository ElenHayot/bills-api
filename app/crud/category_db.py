from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.category import Category

# Get all categories of one user
def get_all_categories(db: Session, user_id: int) -> list[Category]:
    query = select(Category).filter(Category.user_id == user_id)
    
    categories = db.execute(query)
    return categories.scalars().all()

# Find a category by its id and user
def get_category_by_id(db: Session, user_id: int, cat_id: int) -> Category | None:
    query = select(Category).filter(Category.user_id == user_id, Category.cat_id == cat_id)
    category = db.execute(query)
    return category.scalar_one_or_none()

# Find a category by its name and user
def get_category_by_name(db: Session, user_id: int, name: str) -> Category | None:
    query = select(Category).filter(Category.user_id == user_id, Category.name == name)
    category = db.execute(query)
    return category.scalar_one_or_none()

# Add a new category in db
def create_category(db: Session, category: Category) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# Update an existing category
def update_category(db: Session, category: Category, updates: dict) -> Category:
    for key, value in updates.items:
        if hasattr(category, key):
            setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

# Remove a category from db
def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()