# services/auth.py
from sqlalchemy.orm import Session
from models.user import UserModel
from fastapi import HTTPException

class AuthService:
    """
    Service class for authentication related operations
    """

    @staticmethod
    def authenticate_user(email: str, password: str, db: Session) -> UserModel:
        """
        Authenticate a user

        Parameters
        ----------
        email : str
            Email of the user
        password : str
            Password of the user
        db : Session
            Database session

        Returns
        -------
        UserModel
            User model
        """
        
        # Query the database for the user with the provided email
        # user = db.query(UserModel).filter(UserModel.email == email).first()
        user = db.query(UserModel).filter(UserModel.email == email, UserModel.status == 1).first()

        # If the user is not found, raise an HTTPException
        if not user or not user.verify_password(password):
            raise HTTPException(status_code=404, detail="Incorrect email or password.")
        # Return the user
        return user