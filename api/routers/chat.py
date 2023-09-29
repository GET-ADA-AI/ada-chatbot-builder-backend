# /chat
from fastapi import APIRouter, Depends
from api.schemas.chat import ChatCreate, ChatGet
from api.services.chat import ChatService
from api.services.jwt import JwtService
from api.services.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List


chat_router = APIRouter()

# localhost:8000/chat POST
@chat_router.post("/", response_model=ChatGet)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    """
    Create a new chat
    """

    return ChatService.create_chat(chat, db)

@chat_router.get("/{user_id}/{chatbot_id}", response_model=ChatGet)
def get_chat(user_id: int, chatbot_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Get a chat by user id and chatbot id
    """
    return ChatService.get_chat(user_id, chatbot_id, db)
