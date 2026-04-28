from typing import Annotated
from fastapi import APIRouter, Query
from app.schemas.post import PostCreate, PostPublic
from app.services.post import (
    create_post as create_post_service,
    get_posts as get_posts_service,
    delete_post as delete_post_service,
    get_post as get_post_service
)
from app.database import SessionDep

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostPublic)
def create_post(post: PostCreate, session: SessionDep):
    return create_post_service(post, session)


@router.get("/", response_model=list[PostPublic])
def get_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_posts_service(session, offset, limit)
    
@router.get("/{post_id}", response_model=PostPublic)
def get_post(post_id: int, session: SessionDep):
    return get_post_service(post_id, session)

@router.delete("/{post_id}")
def delete_post(post_id: int, session: SessionDep):
    return delete_post_service(post_id, session)