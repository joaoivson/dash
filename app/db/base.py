from sqlalchemy.orm import declarative_base
from app.db.session import engine

# Create declarative base
Base = declarative_base()

# Import all models so Alembic can detect them
from app.models.user import User
from app.models.dataset import Dataset
from app.models.dataset_row import DatasetRow
from app.models.subscription import Subscription


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

