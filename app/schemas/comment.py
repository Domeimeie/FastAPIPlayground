from datetime import datetime
from pydantic import BaseModel, Field

class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    content: str
    date: datetime = Field(default_factory=datetime.now)

class CommentPublic(BaseModel):
    id: int
    date: datetime