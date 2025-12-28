import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.bill import Bill

TITLES = [
    "Supermarket",
    "Restaurant",
    "Train ticket",
    "Cinema",
    "Pharmacy",
    "Gym",
    "Streaming"
]

def random_date_within_last_year():
    now = datetime.now()
    days = random.randint(0, 365)
    return now - timedelta(days=days)

def seed_bills(db: Session, user, categories):
    bills = []

    for _ in range(40):
        category = random.choice(categories)
        bill = Bill(
            title=random.choice(TITLES),
            amount=round(random.uniform(5, 300), 2),
            date=random_date_within_last_year(),
            user_id=user.id,
            category_id=category.id
        )
        db.add(bill)
        bills.append(bill)

    print(f"🧾 {len(bills)} bills created")
