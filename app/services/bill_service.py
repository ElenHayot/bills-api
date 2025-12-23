from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.bill import Bill
from app.schemas.bill import BillBase, BillUpdate
from app.models.user import User
from app.crud import bill_db
from app.services import category_service

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
def get_all_bills(db: Session, current_user: User, category_id: int = None, title: str = None) -> list[Bill]:
    return bill_db.get_all_bills(db, current_user.id, category_id, title)

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
