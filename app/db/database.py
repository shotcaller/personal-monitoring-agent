# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # reconnect if connection dropped
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables if they don't exist. Called on app startup."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()