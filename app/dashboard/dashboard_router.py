"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.user.user_model import User
from app.dashboard.dashboard_schema import DashboardResponse
from app.dashboard import dashboard_service

dashboard_router = APIRouter(tags=["Dashboard"])

# GET : get dashboard global infos
@dashboard_router.get("/", response_model=DashboardResponse,
                      summary="Dashboard data for the current user",
                      description="Returns aggregated bills data for charts and summary")
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), year: int = Query(None)):
    return dashboard_service.get_dashboard(db, current_user, year)