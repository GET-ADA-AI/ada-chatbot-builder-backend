from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.chat import MessageModel #,ChatModel
from api.schemas.chat import MessageCreate, MessageGet #ChatCreate, ChatGet
from api.services.chatbot import ChatbotService
from typing import List
from datetime import datetime

# El ChatService llama al ChatbotModel y este retorna una respuesta  que es la que se da al usuario
class ChatService:
    """
    Service class for chat related operations
    """

    @staticmethod
    def send_message(message: str, db: Session) -> str:
        """
        Send a message to a specific chatbot and receive a response

        Parameters
        ----------
        message : MessageCreate
            Pydantic model for creating a message
        db : Session
            Database Session

        Returns
        -------
        String response
        """

        try:
            # Interface with the chatbot service to get responses from chatbots
            # This part is not implemented, depends on chatbot service implementation
            # Call chatbot service here and add the response as a new message in the chat
            # For example:
            bot_response = ChatbotService.get_response(message)

            # Create a new message instance with the user and chatbot messages
            messageObject = MessageModel(
                user_content=message,
                chatbot_content=bot_response,
                user_id=1,
                chatbot_id=1,
                timestamp=datetime.utcnow()
            )

            # Add the message to the database session
            db.add(messageObject)
            db.commit()
            db.refresh(messageObject)

            return bot_response

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    def get_chat_history(user_id: int, chatbot_id: int, db: Session) -> List[MessageGet]:
        """
        Retrieve chat history by user and chatbot IDs

        Parameters
        ----------
        user_id : int
            ID of the User
        chatbot_id : int
            ID of the ChatBot
        db : Session
            Database Session

        Returns
        -------
        List[MessageGet]
            List of Pydantic models for retrieving messages
        """

        try:
            # Get chat history for the given user_id and chatbot_id
            history = db.query(MessageModel).filter(
                MessageModel.user_id == user_id,
                MessageModel.chatbot_id == chatbot_id
            ).all()

            # Return the chat history
            return history

        except SQLAlchemyError as e:
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

"""
    @staticmethod
    def create_chat(chat: ChatCreate, db: Session) -> ChatGet:
        
        Create a new chat in the PostgreSQL database

        Parameters
        ----------
        chat : ChatCreate
            Pydantic model for creating a chat
        db : Session
            Database Session

        Returns
        -------
        ChatGet
            Pydantic model for retrieving a chat
        

        try:
            # Create a new chat instance
            new_chat = ChatModel(
                header=chat.header,
                user_id=chat.user_id,
                chatbot_id=chat.chatbot_id
            )
            # Add the chat to the database session
            db.add(new_chat)
            # Commit the changes to the database
            db.commit()
            # Refresh the chat to get the chat id
            db.refresh(new_chat)
            # Return the new chat
            return new_chat

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    def get_chat(user_id: int, chatbot_id: int, db: Session) -> ChatGet:
        
        Get chat details and its history from the PostgreSQL database based on user_id and chatbot_id

        Parameters
        ----------
        user_id
        chatbot_id
        db : Session
            Database Session

        Returns
        -------
        Tuple[ChatGet, List[MessageModel]]
            Chat details and list of Pydantic models for retrieving messages
        

        try:
            # Get chat with user_id and chatbot_id
            chat = db.query(ChatModel).filter(
                ChatModel.user_id == user_id,
                ChatModel.chatbot_id == chatbot_id
            ).first()
            # Check if chat exists
            if chat is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="Chat not found")

            # Get chat history for the given user_id and chatbot_id
            history = db.query(MessageModel).filter(
                MessageModel.user_id == user_id,
                MessageModel.chatbot_id == chatbot_id
            ).all()

            # Return the chat
            return chat, history

        except SQLAlchemyError as e:
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)
"""