"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.user.user_model import User
from app.category.category_model import Category
from app.bill.bill_model import Bill
from app.auth.refresh_token import RefreshToken
from app.provider.provider_model import Provider
from app.seeds.users import seed_users
from app.seeds.categories import seed_categories
from app.seeds.bills import seed_bills

def run():
    print("🌱 Seeding development database...")

    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        user = seed_users(db)
        categories = seed_categories(db, user)
        seed_bills(db, user, categories)

        db.commit()
        print("✅ Seed completed")
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run()