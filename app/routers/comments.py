from fastapi import APIRouter
from app.services.comment import (
    create_comment as create_comment_service,
    get_comments as get_comments_service,
    delete_comment as delete_comment_service,
)
from app.schemas.comment import CommentCreate, CommentPublic
from app.database import SessionDep
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentPublic)
def create_comment(comment: CommentCreate, session: SessionDep):
    return create_comment_service(comment, session)

@router.get("/", response_model=list[CommentPublic])
def get_comments(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_comments_service(session, offset, limit)
    

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, session: SessionDep):
    return delete_comment_service(comment_id, session)