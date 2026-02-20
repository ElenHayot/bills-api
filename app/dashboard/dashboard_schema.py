from pydantic import BaseModel
from decimal import Decimal

# Bills group by category
class DashboardCategoryStats(BaseModel):
    category_id: int
    category_name: str
    category_color: str
    nb_bills: int
    total_amount: Decimal

# Bills' global statistics
class DashboardGlobalStats(BaseModel):
    nb_bills: int
    total_amount: Decimal

# Schema send to dashboard
class DashboardResponse(BaseModel):
    year: int
    currency: str = "€"
    global_stats: DashboardGlobalStats
    by_category: list[DashboardCategoryStats]