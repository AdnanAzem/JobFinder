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

    # Relationship with job applications
    applications = relationship("Application", back_populates="user")


# Jobs table: Stores job postings
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String, nullable=False)  
    company = Column(String, nullable=False)  
    location = Column(String, nullable=True) # Job location (remote, city, etc.)  
    description = Column(Text, nullable=True)  # Job description
    requirements = Column(Text, nullable=True) # Job requirements
    posted_at = Column(DateTime, default=datetime.utcnow) # Job posting date  
    source = Column(String, nullable=True) # Job source (e.g., JSearch API) 

    # Relationship with job applications
    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Reference to user
    job_id = Column(Integer, ForeignKey("jobs.id")) # Reference to job
    status = Column(String, default="Pending")  # Application status (Pending, Accepted, Rejected)
    applied_at = Column(DateTime, default=datetime.utcnow) # Timestamp of application submission

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")