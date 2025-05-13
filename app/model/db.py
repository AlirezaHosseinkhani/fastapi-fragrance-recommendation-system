import datetime

from sqlalchemy import Column, Integer, String, DateTime, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create base class for SQLAlchemy models
Base = declarative_base()


# Define your models
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    main_sku = Column(String)
    secondary_skus = Column(JSON)  # SQLite treats this as TEXT, but it works for JSON
    personality = Column(String)


# Create engine and session
SQLALCHEMY_DATABASE_URL = "sqlite:///./recommendations.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
