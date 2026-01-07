from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.db.session import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.models.dataset_row import DatasetRow
from app.schemas.dataset import DatasetResponse, DatasetRowResponse
from app.services.csv_service import CSVService
import pandas as pd
import datetime
import math
from decimal import Decimal
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/datasets", tags=["datasets"])


def get_any_user(db: Session, user_id: int | None = None) -> User:
    query = db.query(User)
    if user_id is not None:
        query = query.filter(User.id == user_id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum usuário encontrado para associar ao dataset")
    return user


def serialize_value(value):
    if value is None:
        return None
    try:
        if isinstance(value, float) and math.isnan(value):
            return None
    except Exception:
        pass
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if isinstance(value, (datetime.date, datetime.datetime, datetime.time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def serialize_row(row: DatasetRow) -> dict:
    return {
        "id": row.id,
        "dataset_id": row.dataset_id,
        "user_id": row.user_id,
        "date": serialize_value(row.date),
        "transaction_date": serialize_value(row.transaction_date),
        "time": serialize_value(row.time),
        "product": row.product,
        "product_name": row.product_name,
        "platform": row.platform,
        "revenue": serialize_value(row.revenue),
        "cost": serialize_value(row.cost),
        "commission": serialize_value(row.commission),
        "profit": serialize_value(row.profit),
        "gross_value": serialize_value(row.gross_value),
        "commission_value": serialize_value(row.commission_value),
        "net_value": serialize_value(row.net_value),
        "quantity": serialize_value(row.quantity),
        "status": row.status,
        "category": row.category,
        "sub_id1": row.sub_id1,
        "mes_ano": row.mes_ano,
        "raw_data": row.raw_data,
    }


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_csv(
    file: UploadFile = File(...),
    user_id: int | None = Query(None),
    db: Session = Depends(get_db)
):
    """Upload e processar arquivo CSV."""
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos CSV são permitidos"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Validate and process CSV
    df, errors = CSVService.validate_csv(file_content, file.filename)
    
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar CSV: {'; '.join(errors)}"
        )
    
    # Create dataset record
    user = get_any_user(db, user_id)
    dataset = Dataset(
        user_id=user.id,
        filename=file.filename
    )
    db.add(dataset)
    db.flush()  # Get dataset.id
    
    # Convert DataFrame to list of dicts
    rows_data = CSVService.dataframe_to_dict_list(df)

    def _sanitize(value):
        if value is None:
            return None
        try:
            if isinstance(value, float) and math.isnan(value):
                return None
        except Exception:
            pass
        try:
            if pd.isna(value):
                return None
        except Exception:
            pass
        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime().isoformat()
        if isinstance(value, (datetime.date, datetime.datetime, datetime.time)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        if hasattr(value, "item"):
            try:
                return value.item()
            except Exception:
                return value
        return value
    
    # Create dataset rows
    dataset_rows = []
    for row_data in rows_data:
        raw_data_json = {k: _sanitize(v) for k, v in row_data.items()} if isinstance(row_data, dict) else row_data
        dataset_row = DatasetRow(
            dataset_id=dataset.id,
            user_id=user.id,
            date=row_data['date'],
            time=row_data.get('time'),
            product=row_data['product'],
            revenue=row_data['revenue'],
            cost=row_data['cost'],
            commission=row_data['commission'],
            profit=row_data['profit'],
            status=row_data.get('status'),
            category=row_data.get('category'),
            sub_id1=row_data.get('sub_id1'),
            mes_ano=row_data.get('mes_ano'),
            raw_data=raw_data_json,
        )
        dataset_rows.append(dataset_row)
    
    db.add_all(dataset_rows)
    db.commit()
    db.refresh(dataset)
    
    # Return response with warnings if any
    if errors:
        # Note: In production, you might want to return warnings differently
        pass
    
    return dataset


@router.get("/latest/rows", response_model=List[DatasetRowResponse])
def list_latest_rows(user_id: int | None = Query(None), db: Session = Depends(get_db)):
    """Listar linhas do dataset mais recente do usuário (ou primeiro usuário)."""
    query = db.query(Dataset)
    if user_id is not None:
        query = query.filter(Dataset.user_id == user_id)
    latest = query.order_by(Dataset.uploaded_at.desc()).first()
    if not latest:
        return []
    rows = db.query(DatasetRow).filter(DatasetRow.dataset_id == latest.id).order_by(DatasetRow.date.desc()).all()
    return JSONResponse(content=[serialize_row(r) for r in rows])


@router.get("", response_model=List[DatasetResponse])
def list_datasets(
    user_id: int | None = Query(None),
    db: Session = Depends(get_db)
):
    """Listar todos os datasets do usuário."""
    query = db.query(Dataset)
    if user_id is not None:
        query = query.filter(Dataset.user_id == user_id)
    datasets = query.order_by(Dataset.uploaded_at.desc()).all()
    
    return datasets


@router.get("/{dataset_id}/rows", response_model=List[DatasetRowResponse])
def list_dataset_rows(dataset_id: int, db: Session = Depends(get_db)):
    """Listar linhas de um dataset específico."""
    rows = db.query(DatasetRow).filter(DatasetRow.dataset_id == dataset_id).order_by(DatasetRow.date.desc()).all()
    return JSONResponse(content=[serialize_row(r) for r in rows])


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """Obter detalhes de um dataset específico."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset não encontrado"
        )
    
    return dataset


@router.post("/{dataset_id}/refresh", response_model=DatasetResponse)
async def refresh_dataset(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Reprocessar/atualizar um dataset.
    
    Nota: Este endpoint está preparado para integração futura com API externa.
    Por enquanto, apenas retorna o dataset existente.
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset não encontrado"
        )
    
    # TODO: Implementar lógica de atualização via API externa quando necessário
    # Por enquanto, apenas retorna o dataset existente
    
    return dataset

