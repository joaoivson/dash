from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class DashboardFilters(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    product: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


class KPIs(BaseModel):
    total_revenue: float
    total_cost: float
    total_commission: float
    total_profit: float
    total_rows: int


class PeriodAggregation(BaseModel):
    period: str  # date or month
    revenue: float
    cost: float
    commission: float
    profit: float
    row_count: int


class ProductAggregation(BaseModel):
    product: str
    revenue: float
    cost: float
    commission: float
    profit: float
    row_count: int


class DashboardResponse(BaseModel):
    kpis: KPIs
    period_aggregations: List[PeriodAggregation]
    product_aggregations: List[ProductAggregation]

