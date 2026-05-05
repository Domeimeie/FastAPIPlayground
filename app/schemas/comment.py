from datetime import datetime
from pydantic import BaseModel, Field

class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    content: str

class CommentPublic(BaseModel):
    id: int
    created_at: datetime