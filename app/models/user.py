from sqlmodel import Field, SQLModel, Relationship
from models.post import Post
from models.comment import Comment

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str
    posts: list["Post"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")
