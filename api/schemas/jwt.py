from pydantic import BaseModel

class Token(BaseModel):
    """
    Pydantic model for a token
    """
    
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None