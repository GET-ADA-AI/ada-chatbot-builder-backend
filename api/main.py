from fastapi import FastAPI
from api.routers.user import user_router
from api.routers.auth import auth_router
from api.routers.chatbot import chatbot_router
from api.services.utils.db import Base, engine

# Create the database tables if they don't exist 
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# App routers
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])

@app.get("/")
async def root():
    """
    Root endpoint for the API that returns a simple message to verify that the API is running.
    """
    return {"message": "Hello World"}