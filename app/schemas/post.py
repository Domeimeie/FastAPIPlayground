from models.user import UserBase
from models.comment import CommentBase    

class PostCreate(PostBase):
    user_id: int

class PostPublic(PostBase):
    id: int
    user: UserBase
    comments: list["CommentBase"] = []