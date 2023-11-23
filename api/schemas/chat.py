from pydantic import BaseModel, Field
from datetime import datetime

class MessageBase(BaseModel):
    """
    Base model for a message
    """

    user_content: str = Field(..., description="Content for the message", min_length=1)

    class Config:
        orm_mode = True

class MessageCreate(MessageBase):
    """
    Pydantic model to create a message
    """
    user_id: int = Field(..., description="ID of the User")
    chatbot_id: int = Field(..., description="ID of the ChatBot")

    class Config:
        from_attributes = True

class MessageGet(MessageBase):
    """
    Pydantic model for retrieving a message
    """
    message_id: int = Field(..., description="ID of the Message")
    chatbot_content: str = Field(..., description="Message of the bot")
    user_id: int = Field(..., description="ID of the User")
    chatbot_id: int = Field(..., description="ID of the ChatBot")
    created_at: datetime = Field(..., description="Creation timestamp of the message")

    class Config:
        orm_mode = True

"""
class ChatBase(BaseModel):
    
    #Base model for a chat
    

    header: str = Field(..., description="Header of the chat", max_length=255, min_length=3)

    class Config:
        from_attributes = True

class ChatCreate(ChatBase):
    
    #Pydantic model to create a chat

    user_id: int = Field(..., description="ID of the User")
    chatbot_id: int = Field(..., description="ID of the ChatBot")

    class Config:
        from_attributes = True

class ChatGet(ChatBase):
    
    #Pydantic model for retrieving a chat
    
    id: int = Field(..., description="ID of the chat")
    created_at: datetime = Field(..., description="Creation timestamp of the chat")
    status: int = Field(..., description="Status of the chat")
    
    class Config:
        from_attributes = True
"""