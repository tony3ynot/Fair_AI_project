from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Ensure proper UTF-8 encoding
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)