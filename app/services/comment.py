from fastapi import HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.schemas.comment import CommentCreate
from app.models.comment import Comment

def create_comment(comment: CommentCreate, session: SessionDep) -> Comment:
    db_comment = Comment.model_validate(comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment

def get_comments(session: SessionDep, offset: int = 0, limit: int = 100) -> list[Comment]:
    comments = session.exec(select(Comment).offset(offset).limit(limit)).all()
    return comments

def delete_comment(comment_id: int, session: SessionDep) -> dict:
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    session.delete(comment)
    session.commit()
    return {"ok": True}