from pydantic import BaseModel, Field
from typing import List, Optional

class ChatBotBase(BaseModel):
    """
    Base model for a chatbot
    """
    chatbot_type: str = Field(..., description="Type of the chatbot", max_length=50)
    user_id: int = Field(..., description="ID of the user who owns the chatbot")

    class Config:
        from_attributes = True  # Using from_attributes here

class ChatbotCreate(ChatBotBase):
    """
    Pydantic model to create a chatbot
    """
    configuration: dict = Field(..., description="Configuration settings for the chatbot")
    data_source_ids: Optional[List[int]] = Field(description="List of data source IDs associated with the chatbot")

class ChatbotGet(ChatBotBase):
    """
    Pydantic model for retrieving a chatbot
    """
    id: int = Field(..., description="ID of the chatbot")
    configuration: dict = Field(..., description="Configuration settings for the chatbot")
    data_source_ids: Optional[List[int]] = Field(description="List of data source IDs associated with the chatbot")

    class Config:
        from_attributes = True  # Using from_attributes here

class ChatbotUpdate(BaseModel):
    """
    Pydantic model for updating a chatbot
    """
    chatbot_type: Optional[str] = Field(None, description="Type of the chatbot", max_length=50)
    configuration: Optional[dict] = Field(None, description="Configuration settings for the chatbot")
    data_source_ids: Optional[List[int]] = Field(None, description="List of data source IDs associated with the chatbot")

    class Config:
        from_attributes = True  # Using from_attributes here
