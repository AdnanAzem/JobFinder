from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# Users table: Stores user details
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    skills = Column(Text, nullable=True) # List of user skills
    resume = Column(Text, nullable=True) # Link to the uploaded resume
    create_at = Column(DateTime, default=datetime.utcnow) # Account creation timestamp

    