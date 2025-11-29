from fastapi import Request, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..database import SessionDep
from datetime import datetime
from ..auth.jwt import verify_access_token
from ..models.user import User

#HttpBearer is responsible for extracting Bearer token from authorization headers

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: SessionDep):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        #validate credentials
        if credentials:
            if credentials.scheme != "Bearer":
                raiseHttpException("invalid authorization scheme. expected \'Bearer\'")
            
            #verify token
            return self.verify_jwt(credentials.credentials, db)
        
        else: 
            raiseHttpException("invalid authorization code")
    
    def verify_jwt(self, token: str, db: SessionDep):
        try:
            payload = verify_access_token(token)
            user_id = payload.get("sub")

            if user_id is None:
                return False
            
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raiseHttpException("user does not exist")
        
            return user
        
        except Exception as e:
            raiseHttpException(f"JWT verification failed: {e}")
        
def raiseHttpException(e, status=status.HTTP_403_FORBIDDEN):
    raise HTTPException(
                status_code=status,
                detail = {
                    "msg": "invalid or expired token",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )


AuthMiddleware = JWTBearer()