from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.bill import Bill
from app.schemas.bill import BillBase, BillUpdate
from app.schemas.dashboard import DashboardCategoryStats, DashboardGlobalStats
from app.models.user import User
from app.crud import bill_db
from app.services import category_service
from datetime import datetime, date
from decimal import Decimal

# Create a new bill
def create_bill(db: Session, current_user: User, bill: BillBase) -> Bill:
    # Verify existing associated category - exception managed in service function
    cat = category_service.get_category_by_id(db, current_user, bill.category_id)
    
    bill_to_create = Bill(
        **bill.model_dump(),
        user_id = current_user.id
    )
    return bill_db.create_bill(db, bill_to_create)

# Get all bills - filtered by current user
def get_all_bills(db: Session, current_user: User, 
                    page: int, page_size: int,
                    category_id: int = None, year: int = None, title: str = None,
                    min_amount: Decimal = None, max_amount: Decimal = None) -> list[Bill]:
    
    offset = (page - 1) * page_size
    return bill_db.get_all_bills(db, current_user.id, category_id, year, title, 
                                 min_amount, max_amount, 
                                 limit=page_size, offset=offset)

# Get an existing bill by its id - filtered by current user
def get_bill_by_id(db: Session, current_user: User, bill_id: int) -> Bill:
    bill = bill_db.get_bill_by_id(db, current_user.id, bill_id)
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Facture inconnue")
    
    return bill

# Update an existing bill
def update_bill(db: Session, current_user: User, bill_id: int, updates: BillUpdate) -> Bill:
    bill = get_bill_by_id(db, current_user, bill_id)

    # Check if user can update this bill
    if current_user.id != bill.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas modifier cette facture.")
  
    # If category changed - verify it exists. Exception managed in service function:
    if updates.category_id:
        cat = category_service.get_category_by_id(db, current_user, updates.category_id)

    update_data = updates.model_dump(exclude_unset=True)
    return bill_db.update_bill(db, bill, update_data)

# Delete an existing bill
def delete_bill(db: Session, current_user: User, bill_id: int):
    bill = get_bill_by_id(db, current_user, bill_id)
    
    # Check if user can delete this bill
    if current_user.id != bill.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas supprimer cette facture.")
  
    return bill_db.delete_bill(db, bill)

# Return bills grouped by category for a chosen year
def get_bills_grouped_by_category(db: Session, current_user: User, year: int = datetime.now().year) -> list[DashboardCategoryStats]:
    result = bill_db.get_bills_grouped_by_category(db, current_user.id, year)
    bill_gb_category = list[DashboardCategoryStats]()
    for row in result:
        bill_gb_category.append(
            DashboardCategoryStats(
                category_name=row.category_name,
                category_color=row.category_color,
                nb_bills=row.nb_bills,
                total_amount=row.total_amount,
                date_year=year
            )
        )
    return bill_gb_category

#Return bills' statistics for a given period
def get_bills_period_statistics(db: Session, current_user: User, date_from: str = None, date_to: str = None) -> list[DashboardGlobalStats]:
    # Initialize period's datetimes
    date_from_dt = None
    date_to_dt = None
    if date_from:
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
    if date_to:
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")
    
    result = bill_db.get_bills_period_statistics(db, current_user.id, date_from_dt, date_to_dt)

    bill_period_stats = DashboardGlobalStats(nb_bills=result.nb_bills, total_amount=result.total_amount)
    return bill_period_stats