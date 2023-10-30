from api.schemas.chatbot import ChatbotCreate, ChatbotGet, ChatbotUpdate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.chatbot import ChatBotModel
import os
from dotenv import load_dotenv
import openai
import pandas as pd
import matplotlib.pyplot as plt
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

# Load environment variables
load_dotenv()

class ChatbotService:
    """
    Service class for chatbot related operations
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = [{"role": "system", "content": "You are a intelligent assistant."}]

    # Train chatbot
    loader = PyPDFLoader("univalle.pdf")
    pages = loader.load_and_split()
    chunks = pages

    # Get embedding model
    embeddings = OpenAIEmbeddings()

    # Create vector database
    db = FAISS.from_documents(chunks, embeddings)

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
                raise HTTPException(status_code=400, detail="User already registered a chatbot")
            # If the chatbot does not exist, create a new chatbot
            new_chatbot = ChatBotModel(
                chatbot_type=chatbot.chatbot_type,
                user_id=chatbot.user_id,
                #configuration=chatbot.configuration,
                #data_source_ids=chatbot.data_source_ids
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
    def patch_chatbot(id: int, chatbot_update: ChatbotUpdate, db: Session) -> ChatbotGet:
        """
        Patch a chatbot in the PostgreSQL database

        Parameters
        ----------
        id : int
            ID of the chatbot to patch
        chatbot_update : ChatbotUpdate
            Pydantic model for updating a chatbot
        db : Session
            Database Session

        Returns
        -------
        ChatbotGet
            Pydantic model for retrieving a chatbot
        """

        try:
            # Get chatbot with id
            chatbot = db.query(ChatBotModel).filter(ChatBotModel.id == id).first()
            # Check if chatbot exists
            if chatbot is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="chatbot not found")
            
            # Update the chatbot attributes
            if chatbot_update.chatbot_type is not None:
                chatbot.chatbot_type = chatbot_update.chatbot_type
            if chatbot_update.user_id is not None:
                chatbot.user_id = chatbot_update.user_id
            
            # Commit the changes to the database
            db.commit()

            # Refresh the chatbot
            db.refresh(chatbot)
            # Return the updated chatbot
            return chatbot

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
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

    @staticmethod
    def get_response(userMessage: str) -> str:
        message = userMessage
        if message:
            ChatbotService.messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=ChatbotService.messages, temperature=0.5
            )

            response = chat.choices[0].message.content
            ChatbotService.messages.append({"role":"assistant", "content":response})
        return response

    @staticmethod
    def get_trained_response(userMessage: str) -> str:
        # Create QA chain to integrate similarity search with user queries (answer query from knowledge base)
        chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

        query = userMessage
        docs = ChatbotService.db.similarity_search(query)

        return chain.run(input_documents=docs, question=query)