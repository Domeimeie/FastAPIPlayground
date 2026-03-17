from fastapi import APIRouter
from app.services.user import create_user as create_user_service
from app.services.user import get_users as get_users_service
from app.services.user import delete_user as delete_user_service
from app.schemas.user import UserPublic, UserCreate
from app.database import SessionDep
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(user: UserCreate, session: SessionDep) -> UserPublic:
    return create_user_service(user, session)


@router.get("/")
def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserPublic]:
    return get_users_service(session, offset, limit)

@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    return delete_user_service(user_id, session)