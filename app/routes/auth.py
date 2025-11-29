from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from ..schemas.auth import LoginRequest, LoginResponse
from ..auth.jwt import create_access_token
from app.database import SessionDep
from datetime import datetime, timedelta
from typing import List
import logging
import bcrypt


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Auth"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(login_request: LoginRequest, db: SessionDep):

    user = db.query(User).filter((login_request.email == User.email)).first()

    #check if user exists
    if not user: 
        raiseHTTPException("user does not exists")
    
    #check if password matches stored password
    password_match = verify_password(login_request.password, user.password)
    
    if not password_match:
        raiseHTTPException("invalid password")


    #generate access token

    claims = {
        "sub": str(user.id),
        "email": user.email,
        "user_id": str(user.id)
    }

    access_token = create_access_token(claims, timedelta(minutes=60))

    return LoginResponse(
        access_token = access_token
    )

def verify_password(plain_text_password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))



def raiseHTTPException(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail={
        "status": "error",
        "message": "Failed to login",
        "timestamp": datetime.utcnow().isoformat()
    }
)

    