from app.schemas.user import UserCreate
from app.models.user import User
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException

def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> List[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

def delete_user(user_id: int, session: SessionDep) -> dict:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}