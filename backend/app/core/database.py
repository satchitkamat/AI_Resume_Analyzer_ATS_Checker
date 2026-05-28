from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load dotenv for env variables
load_dotenv()

# Get database URL from .env
Database_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(Database_URL)

# Create Database Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class For Models
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()