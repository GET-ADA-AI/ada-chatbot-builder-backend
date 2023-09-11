# services/jwt.py
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from models.user import UserModel
from services.utils.db import get_db
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JwtService:
    """
    Service class for JWT related operations
    """

    # Load environment variables for JWT into constants in the class
    # secret key is used to encode the JWT
    SECRET_KEY = os.getenv("SECRET_KEY")
    # algorithm is used to encode the JWT
    ALGORITHM = "HS256"
    # access token expire minutes is the number of minutes the access token is valid for
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    @staticmethod
    def create_access_token(*, user_id: int) -> str:
        """
        Create an access token for a user

        Parameters
        ----------
        user_id : int
            Id of the user

        Returns
        -------
        str
            Access token
        """

        # Create the expire time for the access token 
        expire = datetime.utcnow() + timedelta(minutes=JwtService.ACCESS_TOKEN_EXPIRE_MINUTES)
        # Create the payload for the access token
        to_encode = dict({"id": user_id, "exp": expire})
        # Encode the payload with the secret key and algorithm
        encoded_jwt = jwt.encode(to_encode, JwtService.SECRET_KEY, algorithm=JwtService.ALGORITHM)
        # Return the encoded JWT
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token")), db: Session = Depends(get_db)) -> UserModel:
        """
        Get the current user from the access token

        Parameters
        ----------
        token : str
            Access token, by default Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
        db : Session
            Database session, by default Depends(get_db)

        Returns
        -------
        UserModel
            User model of the current user

        """
        try:
            # Decode the access token
            payload = jwt.decode(token, JwtService.SECRET_KEY, algorithms=[JwtService.ALGORITHM])
            # Get the user id from the payload
            user_id = payload.get("id")
            # If the user id is None, raise an HTTPException
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            # Verify if the expire time of the access token is valid
            if datetime.now() > datetime.fromtimestamp(payload.get("exp")):
                raise HTTPException(status_code=401, detail="Token has expired")

        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Query the database for the user with the provided user id
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        # If the user is not found, raise an HTTPException
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        return user
