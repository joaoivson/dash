from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardFilters, DashboardResponse
from app.api.deps import get_current_user
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    start_date: Optional[date] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data final (YYYY-MM-DD)"),
    product: Optional[str] = Query(None, description="Filtrar por produto (busca parcial)"),
    min_value: Optional[float] = Query(None, description="Valor mínimo"),
    max_value: Optional[float] = Query(None, description="Valor máximo"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter dados do dashboard com KPIs e agregações.
    
    Parâmetros de filtro opcionais:
    - start_date: Data inicial para filtrar os dados
    - end_date: Data final para filtrar os dados
    - product: Nome do produto (busca parcial, case-insensitive)
    - min_value: Valor mínimo para filtrar (aplica-se a revenue, cost, commission ou profit)
    - max_value: Valor máximo para filtrar (aplica-se a revenue, cost, commission ou profit)
    """
    filters = DashboardFilters(
        start_date=start_date,
        end_date=end_date,
        product=product,
        min_value=min_value,
        max_value=max_value
    )
    
    dashboard_data = DashboardService.get_dashboard(
        db=db,
        user_id=current_user.id,
        filters=filters
    )
    
    return dashboard_data

