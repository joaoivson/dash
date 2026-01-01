from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date
from enum import Enum


class DimensionType(str, Enum):
    """Dimensões para agregação."""
    PRODUCT = "product"
    PLATFORM = "platform"
    DATE = "date"


class MetricType(str, Enum):
    """Métricas para análise."""
    GROSS = "gross"  # Total de vendas
    COMMISSION = "commission"  # Comissão
    NET = "net"  # Valor líquido
    QUANTITY = "quantity"  # Quantidade


class AnalyticsFilters(BaseModel):
    """Filtros para análises analíticas."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    product_name: Optional[str] = None
    platform: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


class GlobalKPIs(BaseModel):
    """KPIs globais do dashboard (equivalente ao Power BI)."""
    total_sales: float  # Total de Vendas (Gross Value)
    total_commissions: float  # Total de Comissões
    total_net: float  # Total Líquido
    total_quantity: int  # Quantidade Total de Vendas
    average_ticket: float  # Ticket Médio (gross_value / quantity)
    average_commission: float  # Comissão Média por Venda
    commission_rate: float  # Taxa de Comissão (%)
    net_margin: float  # Margem Líquida (%)


class TimeSeriesPoint(BaseModel):
    """Ponto de série temporal."""
    date: str
    gross_value: float
    commission_value: float
    net_value: float
    quantity: int


class TimeSeriesResponse(BaseModel):
    """Resposta de série temporal."""
    data: List[TimeSeriesPoint]
    period: str  # daily, weekly, monthly


class DimensionBreakdown(BaseModel):
    """Agregação por dimensão (produto ou plataforma)."""
    dimension_value: str  # Nome do produto ou plataforma
    gross_value: float
    commission_value: float
    net_value: float
    quantity: int
    percentage_of_total: float  # % do total


class DimensionBreakdownResponse(BaseModel):
    """Resposta de breakdown por dimensão."""
    dimension: str  # product ou platform
    metric: str  # gross, commission, net
    data: List[DimensionBreakdown]
    total: float


class RankingItem(BaseModel):
    """Item de ranking."""
    rank: int
    name: str  # Nome do produto ou plataforma
    value: float
    percentage: float  # % do total
    quantity: Optional[int] = None


class RankingResponse(BaseModel):
    """Resposta de ranking."""
    type: str  # products_by_sales, products_by_commission, platforms
    metric: str
    data: List[RankingItem]
    limit: int


class GrowthMetrics(BaseModel):
    """Métricas de crescimento."""
    period: str
    current_value: float
    previous_value: float
    growth: float  # Valor absoluto
    growth_percent: float  # Percentual


class FullDashboardResponse(BaseModel):
    """Resposta completa do dashboard (equivalente ao Power BI)."""
    kpis: GlobalKPIs
    time_series: TimeSeriesResponse
    rankings: Dict[str, RankingResponse]  # Múltiplos rankings
    breakdowns: Dict[str, DimensionBreakdownResponse]  # Múltiplos breakdowns
    growth: Optional[List[GrowthMetrics]] = None

