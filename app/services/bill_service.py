from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.bill import Bill
from app.schemas.bill import BillBase, BillUpdate
from app.models.user import User
from app.crud import bill_db, category_db

# Create a new bill
def create_bill(db: Session, current_user: User, bill: BillBase) -> Bill:
    # Verify existing associated category
    cat = category_db.get_category_by_id(bill.category_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catégorie {bill.category_id} inconnue")
    
    bill_to_create = Bill(
        **bill.model_dump(),
        user_id = current_user.id
    )
    return bill_db.create_bill(db, bill_to_create)

# Get all bills
def get_all_bills(db: Session, category_id: int = None, user_id: int = None, title: str = None) -> list[Bill]:
    return bill_db.get_all_bills(db, category_id, user_id, title)

# Get an existing bill by its id
def get_bill_by_id(db: Session, bill_id: int) -> Bill:
    bill = bill_db.get_bill_by_id(db, bill_id)
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Facture inconnue")
    
    return bill

# Update an existing bill
def update_bill(db: Session, current_user: User, bill_id: int, updates: BillUpdate) -> Bill:
    bill = bill_db.get_bill_by_id(bill_id)
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Facture inconnue")

    # Check if user can update this bill
    if current_user.id != bill.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas modifier cette facture.")
  
    # If category changed - verify it exists:
    if updates.category_id:
        cat = category_db.get_category_by_id(updates.category_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catégorie {updates.category_id} inconnue")
          
    update_data = Bill(**updates.model_dump(exclude_unset=True))
    return bill_db.update_bill(db, bill, update_data)

# Delete an existing bill
def delete_bill(db: Session, bill_id: int, current_user: User):
    bill = bill_db.get_bill_by_id(bill_id)
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Facture inconnue")
    
    # Check if user can delete this bill
    if current_user.id != bill.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous ne pouvez pas supprimer cette facture.")
  
    return bill_db.delete_bill(db, bill)
