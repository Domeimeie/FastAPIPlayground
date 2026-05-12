from fastapi import APIRouter
from app.services.user import authenticate_user as authenticate_user_service
from app.schemas.user import UserLogin
from app.database import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(credentials: UserLogin, session: SessionDep) -> str:
    return authenticate_user_service(email=credentials.email, password=credentials.password, session=session)
