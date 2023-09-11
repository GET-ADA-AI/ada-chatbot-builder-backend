# api/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.jwt import Token
from services.auth import AuthService
from services.utils.db import get_db
from sqlalchemy.orm import Session
from services.jwt import JwtService
from schemas.user import UserGet

# Create the auth router
auth_router = APIRouter()

@auth_router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login to get an access token
    """

    # Call the authenticate_user method of the AuthService class to authenticate the user and get the user
    user = AuthService.authenticate_user(form_data.username.strip(), form_data.password, db)
    # Return the access token as a Pydantic model
    return Token(access_token=JwtService.create_access_token(user_id=user.id), token_type="bearer")

@auth_router.get("/me", response_model=UserGet)
def read_users_me(current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint to get the current user
    """
    # Return the current user
    return current_user