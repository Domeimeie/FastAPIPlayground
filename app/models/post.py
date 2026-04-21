from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User

class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")