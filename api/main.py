from fastapi import FastAPI
from api.routers.user import user_router
from api.routers.auth import auth_router
from api.routers.chatbot import chatbot_router
from api.routers.datasource import datasource_router
from api.routers.chat import chat_router
from api.services.utils.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables if they don't exist 
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware to allow preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend's actual URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including OPTIONS
    allow_headers=["*"],
)

# App routers
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(datasource_router, prefix="/datasource", tags=["DataSource"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/")
async def root():
    """
    Root endpoint for the API that returns a simple message to verify that the API is running.
    """
    return {"message": "Hello World"}