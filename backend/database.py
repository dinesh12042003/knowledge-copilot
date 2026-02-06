from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import settings




# SQLite database file
DATABASE_URL = "sqlite:///./chat.db"
DATABASE_URL = settings.DATABASE_URL

# Engine = connection to DB
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session = talking channel with DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
