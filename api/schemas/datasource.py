from pydantic import BaseModel, Field
from datetime import datetime

class DataSourceBase(BaseModel):
    """
    Base model for a datasource
    """

    data_type: str = Field(..., description="Type of document", max_length=5, min_length=2)

    class Config:
        from_attributes = True

class DataSourceCreate(DataSourceBase):
    """
    Pydantic model to create a datasource
    """
    chatbot_id: int = Field(..., description="ID of the ChatBot")

    class Config:
        from_attributes = True

class DataSourceGet(DataSourceBase):
    """
    Pydantic model for retrieving a datasource
    """
    id: int = Field(..., description="ID of the datasource")
    data_type: str = Field(..., description="Document type")
    chatbot_id: int = Field(..., description="ID of the ChatBot")
    created_at: datetime = Field(..., description="Creation timestamp of the datasource")
    status: int = Field(..., description="Status of the datasource")
    
    class Config:
        from_attributes = True
