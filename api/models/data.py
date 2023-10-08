# models/data.py
from sqlalchemy import Column, Integer, DateTime, SmallInteger, String
from api.models.utils.base import BaseModel
import bcrypt

# ELIMINAR
class DataModel(BaseModel):
    """
    Data model that ineherits from BaseModel and maps to the data table in the database.
    """

    # Table name
    __tablename__ = "data"

    # Model's specific attributes
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(255), nullable=False, index=True)