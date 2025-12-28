from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
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