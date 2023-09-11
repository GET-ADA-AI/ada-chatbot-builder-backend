# models/utils/base.py
from services.utils.db import Base
from sqlalchemy import Column, Integer, DateTime, SmallInteger
from datetime import datetime

class BaseModel(Base):
    """
    Base model used to inherit common attributes for all models.
    """
    
    # Setting abstract to true means that this model will not be mapped to a database table
    __abstract__ = True
    
    # Common attributes for all models
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(SmallInteger, default=1)