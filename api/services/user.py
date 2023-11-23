from api.schemas.user import UserCreate, UserGet, UserUpdate, UserUpdatePassword
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.user import UserModel
from typing import List
import bcrypt

class UserService:
    """
    Service class for user related operations
    """

    @staticmethod
    def create_user(user: UserCreate, db: Session) -> UserGet:
        """
        Create a new user in the PostgreSQL database

        Parameters
        ----------
        user : userCreate
            Pydantic model for creating a user
        db : Session
            Database Session

        Returns
        -------
        userGet
            Pydantic model for retrieving a user
        """

        try:
            # Check if user with email already exists
            db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
            # If user exists, raise an HTTPException
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            #If the user does not exist, create a new user
            new_user = UserModel(name=user.name, email=user.email)
            # Password setter will hash the password
            new_user.password = user.password
            # Add the user to the database session
            db.add(new_user)
            # Commit the changes to the database
            db.commit()
            # Refresh the user to get the user id
            db.refresh(new_user)
            # Return the new user
            return new_user

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    def get_user(user_id: int, db: Session) -> UserGet:
        """
        Get all users with status 1 from the PostgreSQL database

        Parameters
        ----------
        db : Session
            Database Session

        Returns
        -------
        List[userGet]
            List of Pydantic models for retrieving users
        """

        try:
            # Get user with user_id
            user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.status == 1).first()
            # Check if user exists
            if user is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="user not found")
            # Return the user
            return user

        except SQLAlchemyError as e:
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)
        
    @staticmethod
    def delete_user(id: int, db: Session):
        """
        Delete a user from the PostgreSQL database

        Parameters
        ----------
        user_id : int
            ID of the user to delete
        db : Session
            Database Session

        Returns
        -------
        userGet
            Pydantic model for retrieving a user
        """

        try:
            # Get user with user_id
            user = db.query(UserModel).filter(UserModel.id == id).first()
            # Check if user exists
            if user is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="user not found")
            
            # Change the status of the user to 0
            user.status = 0
            # Commit the changes to the database
            db.commit()

            # Refresh the user
            db.refresh(user)

            # Return an appropriate message
            return user

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    def update_user_password(id: int, user: UserUpdatePassword, db: Session):
        """
        Update a user's password in the database
        
        Parameters
        ----------
        id : int
            Id of the user
        user : UserUpdatePassword
            Pydantic model for updating a user
        db : Session
            Database session
        """
        try:
            # Get the user from the database
            db_user = db.query(UserModel).filter(UserModel.id == id).first()
            # If the user is not found, raise an HTTPException
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            # If the user is found, verify the password
            print('user.old_password', user.old_password)
            if not db_user.verify_password(user.old_password):
                raise HTTPException(status_code=400, detail="Invalid password")
            print('user.new_password', user.new_password)
            if user.old_password == user.new_password:
                raise HTTPException(status_code=400, detail="New password cannot be the same as old password")
            # If the password is verified, update the user
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            # If the new password is provided, hash the new password
            if user.new_password:
                new_password_hash = bcrypt.hashpw(user.new_password.encode("utf-8"), bcrypt.gensalt())
                setattr(db_user, "_password", new_password_hash)  # Set the hashed password
                db_user.password = user.new_password
            # Commit the changes
            db.commit()
            return {"success": True, "message": "Password updated successfully"}
            
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")