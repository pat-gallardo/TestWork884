from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)