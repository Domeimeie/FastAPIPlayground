from fastapi import APIRouter
from app.services.post import create_post as create_post_service
from app.services.post import get_posts as get_posts_service
from app.services.post import delete_post as delete_post_service
from app.schemas.user import PostPublic, PostCreate
from app.database import SessionDep
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/")
def create_post(post: PostCreate, session: SessionDep) -> PostPublic:
    return create_post_service(post, session)


@router.get("/")
def get_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[PostPublic]:
    return get_posts_service(session, offset, limit)

@router.delete("/{post_id}")
def delete_post(post_id: int, session: SessionDep):
    return delete_post_service(post_id, session)