from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, Date, Boolean, Text, UniqueIdentifier

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"
    user_id = Column(UniqueIdentifier, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(50), nullable=False)

# Define other models (Properties, Taxes, etc.) similarly
