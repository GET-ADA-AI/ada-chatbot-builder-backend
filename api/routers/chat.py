# /chat
from fastapi import APIRouter, Depends
from api.schemas.chat import MessageCreate, MessageGet #ChatCreate, ChatGet
from api.services.chat import ChatService
from api.services.jwt import JwtService
from api.services.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List


chat_router = APIRouter()

# POST /message
@chat_router.post("/")
def send_message(message: str, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Send a message to a specific chatbot and receive a response
    """

    return ChatService.send_message(message, db)

@chat_router.post("/trained")
def send_trained_message(message: str, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Send a message to a specific trained chatbot and receive a response
    """

    return ChatService.send_trained_message(message, db)

# GET /message/{user_id}/{chatbot_id}
@chat_router.get("/{user_id}/{chatbot_id}", response_model=List[MessageGet])
def get_chat_history(user_id: int, chatbot_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Retrieve chat history by user and chatbot IDs
    """

    return ChatService.get_chat_history(user_id, chatbot_id, db)

"""
# localhost:8000/chat POST
@chat_router.post("/", response_model=ChatGet)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    
    #Create a new chat
    

    return ChatService.create_chat(chat, db)

# GET /chat/{user_id}/{chatbot_id}
@chat_router.get("/{user_id}/{chatbot_id}", response_model=ChatGet)
def get_chat(user_id: int, chatbot_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    
    #Protected endpoint
    #Get a chat by user id and chatbot id
    

    return ChatService.get_chat(user_id, chatbot_id, db)
"""