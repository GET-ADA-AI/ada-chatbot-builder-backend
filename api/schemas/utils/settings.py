from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    # Add other configurations here

settings = Settings()