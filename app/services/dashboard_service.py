from sqlalchemy.orm import Session
from app.schemas.dashboard import DashboardResponse
from app.models.user import User
from app.services import bill_service
from datetime import datetime

def get_dashboard(db: Session, current_user: User, year: int = datetime.now().year) -> DashboardResponse:
    if not year:
        year = datetime.now().year
    
    # Get global statistic for current year
    global_stats = bill_service.get_bills_period_statistics(db, current_user,f"{year}-01-01", f"{year}-12-31")
    by_category = bill_service.get_bills_grouped_by_category(db, current_user, year)
    
    response = DashboardResponse(year = year, currency="€", global_stats=global_stats, by_category=by_category)
    return response