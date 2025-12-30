from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class DatasetRow(Base):
    __tablename__ = "dataset_rows"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    product = Column(String, nullable=False, index=True)
    revenue = Column(Numeric(12, 2), nullable=False)
    cost = Column(Numeric(12, 2), nullable=False)
    commission = Column(Numeric(12, 2), nullable=False)
    profit = Column(Numeric(12, 2), nullable=False)

    # Relationships
    dataset = relationship("Dataset", back_populates="rows")
    user = relationship("User", back_populates="dataset_rows")

    # Composite indexes for analytics queries
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date'),
        Index('idx_user_product', 'user_id', 'product'),
        Index('idx_user_date_product', 'user_id', 'date', 'product'),
    )

