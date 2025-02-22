from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    content = Column(String)
    skills = Column(String)

class JobListing(Base):
    __tablename__ = 'job_listings'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    company = Column(String)
    location = Column(String)

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    job_id = Column(Integer)
    score = Column(Float)

# Database connection
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)