from sqlmodel import Field, SQLModel, Relationship
from models.user import User
from models.post import Post

class CommentBase(SQLModel):
    content: str

class Comment(CommentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    post: Post | None = Relationship(back_populates="comments")
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="comments")
