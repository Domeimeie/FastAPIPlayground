from sqlmodel import SQLModel, Field, Relationship
from app.models.post import Post
from app.models.user import User

class Comment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    post_id: int = Field(foreign_key="post.id")
    post: Post | None = Relationship(back_populates="comments")
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="comments")