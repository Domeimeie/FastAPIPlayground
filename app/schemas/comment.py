from models.user import UserBase
from models.post import PostBase

class CommentCreate(CommentBase):
    post_id: int
    user_id: int

class CommentPublic(CommentBase):
    id: int
    post: PostBase
    user: UserBase
