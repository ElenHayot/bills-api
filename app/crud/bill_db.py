from sqlalchemy.orm import Session
from sqlalchemy import select, func, extract
from app.models.bill import Bill
from app.models.category import Category
from datetime import datetime
from decimal import Decimal

# Get all bills of one user
def get_all_bills(db: Session, user_id: int,
                    category_id: int = None, year: int = None, title: str = None,
                    min_amount: Decimal = None, max_amount: Decimal = None,
                    limit: int = None, offset: int = None) -> list[Bill]:
    
    query = select(Bill).filter(Bill.user_id == user_id).order_by(Bill.date.desc(), Bill.id.desc())

    if category_id:
        query = query.filter(Bill.category_id == category_id)
    if year:
        query = query.filter(extract("year", Bill.date) == year)
    if title:
        query = query.filter(Bill.title.ilike(f"%{title}%"))
    if min_amount:
        query = query.filter(Bill.amount >= min_amount)
    if max_amount:
        query = query.filter(Bill.amount <= max_amount)

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    
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
    for key, value in updates.items():
        if hasattr(bill, key):
            setattr(bill, key, value)
    db.commit()
    db.refresh(bill)
    return bill

# Delete a bill from db
def delete_bill(db: Session, bill: Bill):
    db.delete(bill)
    db.commit()

# Get bills grouped by category, filtered on a given year
def get_bills_grouped_by_category(db: Session, user_id: int, year: int):
    query = (
        select(
            Category.name.label("category_name"),
            Category.color.label("category_color"),
            func.count(Bill.id).label("nb_bills"),
            func.sum(Bill.amount).label("total_amount")
        )
        .join(Bill, Bill.category_id == Category.id)
        .filter(Bill.user_id == user_id)
        .filter(extract("year", Bill.date) == year)
        .group_by(Category.id, Category.name, Category.color)
    )

    return db.execute(query)

# Get bills' statistics for a given period
def get_bills_period_statistics(db: Session, user_id: int, date_from: datetime, date_to: datetime):
    query = (
        select(
            func.count(Bill.id).label("nb_bills"),
            func.coalesce(func.sum(Bill.amount), 0).label("total_amount")
        )
        .filter(Bill.user_id == user_id)
    )
    if date_from:
        query = query.filter(Bill.date >= date_from)
        
    if date_to:
        query = query.filter(Bill.date <= date_to)
    
    return db.execute(query).one()
