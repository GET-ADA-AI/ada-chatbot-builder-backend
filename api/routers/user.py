# /user
from fastapi import APIRouter, Depends
from api.schemas.user import UserCreate, UserGet, UserUpdate, UserUpdatePassword
from api.services.user import UserService
from api.services.jwt import JwtService
from api.services.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter()

# Esto apunta a: localhost:8000/user POST
@user_router.post("/", response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """

    return UserService.create_user(user, db)

@user_router.get("/{user_id}", response_model=UserGet)
def get_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Get a user by id
    """
    return UserService.get_user(user_id, db)

@user_router.delete("/{user_id}", response_model=UserGet)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Delete a user by id
    """
    return UserService.delete_user(user_id, db)

@user_router.patch("/password")
def update_user_password(user_update_password: UserUpdatePassword, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    Update a user password using it's id
    """
    # Call the update_user_password method of the UserService class
    return UserService.update_user_password(current_user.id, user_update_password, db)
