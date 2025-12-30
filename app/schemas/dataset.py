from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DatasetBase(BaseModel):
    filename: str


class DatasetCreate(DatasetBase):
    pass


class DatasetResponse(DatasetBase):
    id: int
    user_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DatasetRowBase(BaseModel):
    date: str
    product: str
    revenue: float
    cost: float
    commission: float


class DatasetRowCreate(DatasetRowBase):
    profit: float


class DatasetRowResponse(DatasetRowBase):
    id: int
    dataset_id: int
    user_id: int
    profit: float

    class Config:
        from_attributes = True

