from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class ChatCreate(BaseModel):
    question: str

class ChatOut(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: datetime

    class Config:
        orm_mode = True
