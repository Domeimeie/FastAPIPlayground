from app.models.post import Post
from app.schemas.post import PostCreate
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException

def create_post(post: PostCreate, session: SessionDep):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

def get_posts(session: SessionDep, offset: int = 0, limit: int = 100):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts

def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"ok": True}