"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy.orm import Session
from app.category.category_model import Category

CATEGORIES = [
    ("Food", "#FF6B6B"),
    ("Rent", "#4ECDC4"),
    ("Transport", "#FFD93D"),
    ("Health", "#1A535C"),
    ("Entertainment", "#5F27CD"),
]

def seed_categories(db: Session, user):
    categories = []

    for name, color in CATEGORIES:
        category = (
            db.query(Category)
            .filter_by(user_id=user.id, name=name)
            .first()
        )
        if category:
            categories.append(category)
            continue

        category = Category(
            name=name,
            color=color,
            user_id=user.id
        )
        db.add(category)
        categories.append(category)

    db.flush()
    print(f"📁 {len(categories)} categories ready")
    return categories