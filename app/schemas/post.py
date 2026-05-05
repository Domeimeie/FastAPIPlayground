
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.user import User

class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str
    date: datetime = Field(default_factory=datetime.now)

class PostPublic(BaseModel):
    id: int
    user: User
    title: str
    content: str
    date: datetime