from jose import jwt, JWTError
from datetime import timedelta, datetime
import os 
from typing import Optional


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRATION_MINUTES =int(os.getenv("JWT_EXPIRATION_TIME"))


def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expiration_time = datetime.utcnow() + expires_delta
    else:
        expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)

    claims.update({"exp": expiration_time})

    return jwt.encode(claims, SECRET_KEY, ALGORITHM)

def verify_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except JWTError as e:
        raise e