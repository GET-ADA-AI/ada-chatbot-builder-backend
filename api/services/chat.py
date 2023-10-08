from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.chat import MessageModel #,ChatModel
from api.schemas.chat import MessageCreate, MessageGet #ChatCreate, ChatGet
from typing import List

# El ChatService llama al ChatbotModel y este retorna una respuesta  que es la que se da al usuario
class ChatService:
    """
    Service class for chat related operations
    """

    @staticmethod
    def send_message(message: MessageCreate, db: Session) -> List[MessageGet]:
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
        List[MessageGet]
            List of Pydantic models for retrieving messages
        """

        try:
            # Create a new user_message instance
            user_message = MessageModel(
                content=message.content,
                user_id=message.user_id,
                chatbot_id=message.chatbot_id,
                is_user_message=True,
                timestamp=datetime.utcnow()
            )

            # Interface with the chatbot service to get responses from chatbots
            # This part is not implemented, depends on chatbot service implementation
            # Call chatbot service here and add the response as a new message in the chat
            # For example:
            # bot_response = chatbot_service.get_response(message.content)

            # Create a new bot_message instance
            bot_message = MessageModel(
                content=bot_response,
                user_id=message.user_id,
                chatbot_id=message.chatbot_id,
                is_user_message=False,
                timestamp=datetime.utcnow()
            )

            # Add the message to the database session
            db.add(user_message)
            db.commit()
            db.refresh(user_message)

            db.add(bot_message)
            db.commit()
            db.refresh(bot_message)

            return user_message, bot_message

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