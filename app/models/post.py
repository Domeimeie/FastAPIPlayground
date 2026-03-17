from sqlmodel import Field, SQLModel, Relationship
from models.user import User
from models.comment import Comment

class PostBase(SQLModel):
    title: str
    content: str

class Post(PostBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")
