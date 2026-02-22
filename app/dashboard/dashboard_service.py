"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy.orm import Session
from app.dashboard.dashboard_schema import DashboardResponse
from app.user.user_model import User
from app.bill import bill_service
from datetime import datetime

def get_dashboard(db: Session, current_user: User, year: int = datetime.now().year) -> DashboardResponse:
    if not year:
        year = datetime.now().year
    
    # Get global statistic for current year
    global_stats = bill_service.get_bills_period_statistics(db, current_user,f"{year}-01-01", f"{year}-12-31")
    by_category = bill_service.get_bills_grouped_by_category(db, current_user, year)
    
    response = DashboardResponse(year = year, currency="€", global_stats=global_stats, by_category=by_category)
    return response