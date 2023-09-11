from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the engine with the base arguments for the DB connection
engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={
        "sslmode": "require",
        "application_name": "my_app",
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
        "password":os.getenv("DATABASE_PASSWORD")
    }
)

# Create a session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base for auto-migrations
Base = declarative_base()

def get_db() -> Session:
    """
    Initialize a new database session,
    yield it to the caller for database operations,
    and close the session when the caller is done.
    """
    
    # Initialize a new session
    db = SessionLocal()
    try:
        # Yield the session to the caller
        yield db
    finally:
        # Close the session 
        db.close()