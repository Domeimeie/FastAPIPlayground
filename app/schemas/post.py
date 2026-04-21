from pydantic import BaseModel
from app.models.user import User

class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str

class PostPublic(BaseModel):
    id: int
    user: User