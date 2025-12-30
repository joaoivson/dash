from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.db.session import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.models.dataset_row import DatasetRow
from app.schemas.dataset import DatasetResponse, DatasetRowResponse
from app.api.deps import get_current_user
from app.services.csv_service import CSVService

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
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
    dataset = Dataset(
        user_id=current_user.id,
        filename=file.filename
    )
    db.add(dataset)
    db.flush()  # Get dataset.id
    
    # Convert DataFrame to list of dicts
    rows_data = CSVService.dataframe_to_dict_list(df)
    
    # Create dataset rows
    dataset_rows = []
    for row_data in rows_data:
        dataset_row = DatasetRow(
            dataset_id=dataset.id,
            user_id=current_user.id,
            date=row_data['date'],
            product=row_data['product'],
            revenue=row_data['revenue'],
            cost=row_data['cost'],
            commission=row_data['commission'],
            profit=row_data['profit']
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


@router.get("", response_model=List[DatasetResponse])
def list_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todos os datasets do usuário."""
    datasets = db.query(Dataset).filter(
        Dataset.user_id == current_user.id
    ).order_by(
        Dataset.uploaded_at.desc()
    ).all()
    
    return datasets


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de um dataset específico."""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset não encontrado"
        )
    
    return dataset


@router.post("/{dataset_id}/refresh", response_model=DatasetResponse)
async def refresh_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reprocessar/atualizar um dataset.
    
    Nota: Este endpoint está preparado para integração futura com API externa.
    Por enquanto, apenas retorna o dataset existente.
    """
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset não encontrado"
        )
    
    # TODO: Implementar lógica de atualização via API externa quando necessário
    # Por enquanto, apenas retorna o dataset existente
    
    return dataset

