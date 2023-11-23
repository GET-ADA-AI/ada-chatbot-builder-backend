# /chatbot
from fastapi import APIRouter, Depends
from api.schemas.chatbot import ChatbotCreate, ChatbotGet, ChatbotUpdate
from api.services.chatbot import ChatbotService
from api.services.jwt import JwtService
from api.services.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List


chatbot_router = APIRouter()

# localhost:8000/chatbot POST
@chatbot_router.post("/", response_model=ChatbotGet)
def create_chatbot(chatbot: ChatbotCreate, db: Session = Depends(get_db)):
    """
    Create a new chatbot
    """

    return ChatbotService.create_chatbot(chatbot, db)

@chatbot_router.get("/{chatbot_id}", response_model=ChatbotGet)
def get_chatbot(chatbot_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Get a chatbot by id
    """
    return ChatbotService.get_chatbot(chatbot_id, db)

@chatbot_router.delete("/{chatbot_id}", response_model=ChatbotGet)
def delete_chatbot(chatbot_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Delete a chatbot by id
    """
    return ChatbotService.delete_chatbot(chatbot_id, db)

@chatbot_router.patch("/{chatbot_id}", response_model=ChatbotGet)
def patch_chatbot(chatbot_id: int, chatbot_update: ChatbotUpdate, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Patch a chatbot by id
    """
    return ChatbotService.patch_chatbot(chatbot_id, chatbot_update, db)
