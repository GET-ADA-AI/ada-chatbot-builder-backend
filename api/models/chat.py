# models/chat.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from api.models.utils.base import BaseModel
from datetime import datetime
"""
class ChatModel(BaseModel):
    
    #Chat model that ineherits from BaseModel and maps to the chat table in the database.
    

    # Table name
    __tablename__ = "chat"

    # Model's specific attributes
    header = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    chatbot_id = Column(Integer, nullable=False, index=True)

    # Relationships
    messages = relationship('MessageModel', back_populates='chat')

    def send_message(self, content, is_user_message=True):
        
        Send a message in the chat.
        Args:
            content (str): The content of the message.
            is_user_message (bool): True if the message is sent by the user, False if by the chatbot.
        Returns:
            MessageModel: The sent message.
        
        # Create a new message instance
        message = MessageModel(
            content=content,
            user_id=self.user_id,
            chatbot_id=self.chatbot_id,
            is_user_message=is_user_message,
            timestamp=datetime.utcnow()
        )
        # Add the message to the chat's messages
        self.messages.append(message)
        return message
"""

class MessageModel(BaseModel):
    """
    Message model that inherits from BaseModel and maps to the message table in the database.
    """

    # Table name
    __tablename__ = "message"

    # Model's specific attributes
    # Incluir mensaje de usuario y respuesta del chatbot
    content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)
    chatbot_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_user_message = Column(Boolean, nullable=False)

"""
    # Foreign Key relationship to ChatModel
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('ChatModel', back_populates='messages')
"""