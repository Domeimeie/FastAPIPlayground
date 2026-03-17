from models.post import PostBase
from models.comment import CommentBase

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int
    posts: list["PostBase"] = []
    comments: list["CommentBase"] = []
