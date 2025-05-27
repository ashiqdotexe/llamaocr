from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from database.ocr_database import Base


# User Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    service = Column(String, default="passport", nullable=False)
    chat_history = relationship("ChatHistory", back_populates="user")


# Chat History Table
class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    search_history = Column(Text, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="chat_history")
