from app.schemas import CommentCreate
from app.models import Comment
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException

def create_comment(comment: CommentCreate, session: SessionDep) -> CommentPublic:
    db_comment = Comment.model_validate(comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment

def get_comments(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[CommentPublic]:
    comments = session.exec(select(Comment).offset(offset).limit(limit)).all()
    return comments

def delete_comment(comment_id: int, session: SessionDep):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    session.delete(comment)
    session.commit()
    return {"ok": True}