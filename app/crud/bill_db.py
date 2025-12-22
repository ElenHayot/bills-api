from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.bill import Bill

# Get all bills of one user
def get_all_bills(db: Session, user_id: int, category_id: int = None, title: str = None) -> list[Bill]:
    query = select(Bill).filter(Bill.user_id == user_id)

    if category_id:
        query = query.filter(Bill.category_id == category_id)
    if title:
        query = query.filter(Bill.title.ilike(f"%{title}%"))
    
    bills = db.execute(query)
    return bills.scalars().all()

# Find a bill by its id and user
def get_bill_by_id(db: Session, user_id: int, bill_id: int) -> Bill | None:
    query = select(Bill).filter(Bill.user_id == user_id, Bill.id == bill_id)
    bill = db.execute(query)
    return bill.scalar_one_or_none()

# Add a new bill in db
def create_bill(db: Session, bill: Bill) -> Bill:
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill

# Update an existing bill
def update_bill(db: Session, bill: Bill, updates: dict) -> Bill:
    for key, value in updates.items:
        if hasattr(bill, key):
            setattr(bill, key, value)
    db.commit()
    db.refresh(bill)
    return bill

# Delete a bill from db
def delete_bill(db: Session, bill: Bill):
    db.delete(bill)
    db.commit()