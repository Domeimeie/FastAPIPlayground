from fastapi import HTTPException, Query
from fastapi import APIRouter
from fastapi import Query
from app.services.comment import create_comment as create_comment_service
from app.services.comment import get_comment as get_comment_service
from app.services.comment import delete_comment as delete_comment_service
from app.schemas.user import CommentPublic, CommentCreate
from app.database import SessionDep
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/")
def create_comment(comment: CommentCreate, session: SessionDep) -> CommentPublic:
    return create_comment_service(comment, session)


@router.get("/")
def get_comments(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[CommentPublic]:
    return get_comment_service(session, offset, limit)
    


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, session: SessionDep):
    return delete_comment_service(comment_id)