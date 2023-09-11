from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

class UserBase(BaseModel):
    """
    Base model for a user
    """

    name: str = Field(..., description="Name of the person or business", max_length=255, min_length=3)
    email: EmailStr = Field(..., description="Email of the person or business")

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    """
    Pydantic model to create a user
    """
    password: str = Field(..., description="Password of the user", max_length=255, min_length=8)
    password_confirmation: str = Field(..., description="Password confirmation of the user")

    @validator('password_confirmation')
    def passwords_match(cls, v, values, **kwargs):
        """
        Pydantic validator to check if the password and password confirmation match
        """
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        from_attributes = True

class UserGet(UserBase):
    """
    Pydantic model for retrieving a user
    """
    id: int = Field(..., description="ID of the user")
    created_at: datetime = Field(..., description="Creation timestamp of the user")
    status: int = Field(..., description="Status of the user")
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """
    Pydantic model for updating a user
    """
    name: str = Field(None, description="Name of the person or business", max_length=255, min_length=3)
    email: EmailStr = Field(None, description="Email of the person or business")
    
    class Config:
        from_attributes = True

class UserUpdatePassword(BaseModel):
    """
    Pydantic model for updating a user's password
    """

    old_password: str = Field(None, description="Password of the user", max_length=255, min_length=8)
    new_password: str = Field(None, description="Password of the user", max_length=255, min_length=8)
    new_password_confirmation: str = Field(None, description="Password confirmation of the user")

    @validator('new_password_confirmation')
    def passwords_match(cls, v, values, **kwargs):
        """
        Pydantic validator to check if the password and password confirmation match
        """
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    class Config:
        from_attributes = True