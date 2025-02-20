from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a database engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Configure the session to interact with the database
SessionLacal = sessionmaker(autocommit= False,autoflush = False, bind = engine)

# Define the base class for SQLAlchemy models
Base = declarative_base()