# models/user.py
from sqlalchemy import Column, Integer, DateTime, SmallInteger, String
from api.models.utils.base import BaseModel
import bcrypt

class UserModel(BaseModel):
    """
    User model that ineherits from BaseModel and maps to the user table in the database.
    """

    # Table name
    __tablename__ = "user"

    # Model's specific attributes
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    
    # Atribute to store the hashed password is private
    _password = Column("password", String(255), nullable=False)
    
    @property
    def password(self):
        """
        Getter method for the password field

        This property raises an AttributeError since the password attribute is not readable.
        """
        return AttributeError("Password is not readable atrribute")

    @password.setter
    def password(self, password):
        """
        Setter method for the password field

        This property hashes the password using bcrypt and stores the hash in the _password field.

        Parameters
        ----------
        password : str
            Password to hash
        """
        try:
            # If your database expects a string, decode the hashed password
            self._password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
        except Exception as e:
            print(f"An error occurred while hashing the password: {e}")

    
    def verify_password(self, password: str) -> bool:
        try:
            password_bytes = password.encode("utf-8")
            return bcrypt.checkpw(password_bytes, self._password.encode("utf-8"))
        except ValueError as e:
            print(f"An error occurred: {e}")
            return False
