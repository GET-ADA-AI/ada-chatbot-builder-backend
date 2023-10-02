from api.schemas.chatbot import ChatbotCreate, ChatbotGet
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.chatbot import ChatBotModel  # Corrected the import path

class ChatbotService:
    """
    Service class for chatbot related operations
    """

    @staticmethod
    def create_chatbot(chatbot: ChatbotCreate, db: Session) -> ChatbotGet:
        """
        Create a new chatbot in the PostgreSQL database

        Parameters
        ----------
        chatbot : chatbotCreate
            Pydantic model for creating a chatbot
        db : Session
            Database Session

        Returns
        -------
        chatbotGet
            Pydantic model for retrieving a chatbot
        """
        try:
            # Check if chatbot with the same user_id already exists
            db_chatbot = db.query(ChatBotModel).filter(ChatBotModel.user_id == chatbot.user_id).first()
            # If chatbot exists, raise an HTTPException
            if db_chatbot:
                raise HTTPException(status_code=400, detail="User ID already registered")
            # If the chatbot does not exist, create a new chatbot
            new_chatbot = ChatBotModel(
                chatbot_type=chatbot.chatbot_type,
                user_id=chatbot.user_id,
                configuration=chatbot.configuration,
                data_source_ids=chatbot.data_source_ids
            )
            # Add the chatbot to the database session
            db.add(new_chatbot)
            # Commit the changes to the database
            db.commit()
            # Refresh the chatbot to get the chatbot id
            db.refresh(new_chatbot)
            # Return the new chatbot
            return new_chatbot

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    def get_chatbot(chatbot_id: int, db: Session) -> ChatbotGet:
        """
        Get a chatbot with status 1 from the PostgreSQL database

        Parameters
        ----------
        db : Session
            Database Session

        Returns
        -------
        chatbotGet
            Pydantic model for retrieving a chatbot
        """
        try:
            # Get chatbot with chatbot_id
            chatbot = db.query(ChatBotModel).filter(ChatBotModel.id == chatbot_id).first()
            # Check if chatbot exists
            if chatbot is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="chatbot not found")
            # Return the chatbot
            return chatbot

        except SQLAlchemyError as e:
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    def delete_chatbot(id: int, db: Session):
        """
        Delete a chatbot from the PostgreSQL database

        Parameters
        ----------
        chatbot_id : int
            ID of the chatbot to delete
        db : Session
            Database Session
        """
        try:
            # Get chatbot with chatbot_id
            chatbot = db.query(ChatBotModel).filter(ChatBotModel.id == id).first()
            # Check if chatbot exists
            if chatbot is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="chatbot not found")
            # Delete the chatbot from the database
            db.delete(chatbot)
            # Commit the changes to the database
            db.commit()

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)
