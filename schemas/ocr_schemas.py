from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# Schema for User
class UserBase(BaseModel):
    user_id: str
    url: HttpUrl
    service: Optional[str] = "passport"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Schema for ChatHistory
class ChatHistoryBase(BaseModel):
    user_id: int
    search_history: Optional[str] = None

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistoryResponse(ChatHistoryBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
