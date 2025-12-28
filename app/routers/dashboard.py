from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services import dashboard_service

dashboard_router = APIRouter(tags=["Dashboard"])

# GET : get dashboard global infos
@dashboard_router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), year: int = Query(None)):
    return dashboard_service.get_dashboard(db, current_user, year)