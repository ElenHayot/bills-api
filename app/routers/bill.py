from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.bill import BillBase, BillRead, BillUpdate
from app.services import bill_service

bill_router = APIRouter(tags=["Bills"])

# POST : Create a bill for the current user
@bill_router.post("/", response_model=BillRead)
def create(bill_data: BillBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return bill_service.create_bill(db, current_user, bill_data)

# GET : Get all bills, filtered by current user
@bill_router.get("/", response_model=list[BillRead])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return bill_service.get_all_bills(db, current_user)

# GET : Get one bill by its ID, filtered by current user
@bill_router.get("/{bill_id}", response_model=BillRead)
def read(bill_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return bill_service.get_bill_by_id(db, current_user, bill_id)

# PUT : Update a current user's bill
@bill_router.put("/{bill_id}", response_model=BillRead)
def update(bill_id: int, updates: BillUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return bill_service.update_bill(db, current_user, bill_id, updates)

# DELETE : Delete a bill from the current user
@bill_router.delete("/{bill_id}")
def delete(bill_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return bill_service.delete_bill(db, current_user, bill_id)
