from fastapi import APIRouter, Depends, Request, HTTPException, status, File, UploadFile
from ..models.user import User
from ..schemas.user import UserCreateRequest, UserUpdateRequest, UserResponse 
from ..database import SessionDep
from ..middleware.auth import AuthMiddleware
from ..utils.response import ResponseModel, response
from datetime import datetime
import logging
import pymysql
import bcrypt
import aiofiles
import os


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Users"]
)

UPLOAD_DIR = "static/profile"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[UserResponse])
def create(user_request: UserCreateRequest, db: SessionDep, request: Request):

    user_exists = db.query(User).filter((user_request.email == User.email)).first()

    if user_exists: 
        raiseError("User already exists", request)
    
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    
    new_user = User(
        **user_request.dict(exclude={"password", "confirm_password"}),
        password=hashed_password.decode(),
    )

    try:  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return response(new_user, "User created successfully")
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)



@router.get("/me", status_code=status.HTTP_200_OK, response_model = ResponseModel[UserResponse])
def get_current_user(current_user = Depends(AuthMiddleware)):
    return response(current_user, "User retrieved successfully")

@router.post("/me/upload", status_code=status.HTTP_200_OK)
async def upload_product(db: SessionDep, request: Request, image: UploadFile = File(None), current_user = Depends(AuthMiddleware)):

    if not image:
        raiseError("Please upload image", request, status.HTTP_400_BAD_REQUEST)

    allowed_ext = ["png", "jpeg", "jp"]
    file_ext = image.filename.split(".")[-1].lower()

    if not file_ext in  allowed_ext:
        raiseError("Invalid file extension", request, status.HTTP_400_BAD_REQUEST)

    max_image_size = 1024 * 1024
    content = await image.read()
    if len(content) > max_image_size:
        raiseError("File too large. Maximum size allowed is 1 MB.", request,  status.HTTP_400_BAD_REQUEST)

    await image.seek(0)

    try:
    
        file_name = f"{current_user.id}.{file_ext}"

        file_path = f"{UPLOAD_DIR}/{file_name}"
        print(file_path)

        async with aiofiles.open(file_path, "wb") as output_file:
            content = await image.read()
            await output_file.write(content)

    except:
        raiseError("Internal Server Error", request, status.HTTP_500_INTERNAL_SERVER_ERROR)

    image_url = f"http://localhost:8000/static/profile/{file_name}"
    current_user.image_url = image_url
    
    try:
        db.commit()
        db.refresh(current_user)
        return {
            "message": "Upload successful", 
            "image_url": image_url
        }
    except pymysql.DataError as e:
        raiseError(e, request) 
    except Exception as e:
        raiseError(e, request)



@router.put("/me", status_code=status.HTTP_200_OK, response_model=ResponseModel[UserResponse])
def update_user(user_request: UserUpdateRequest, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):

    update_data = user_request.dict(exclude_unset=True)

    try:
        for field, value in update_data.items():
            setattr(current_user, field, value)
        db.commit()
        db.refresh(current_user)
        return response(current_user, "User updated successfully")
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)



def raiseError(e: str, request: Request, status_code = status.HTTP_400_BAD_REQUEST):
 
    method = request.method.upper()

    if method == "POST":
        message = f"Failed to create record: {e}"
    elif method == "GET":
        message = f"Failed to fetch record: {e}"
    elif method in ("PUT", "PATCH"):
        message = f"Failed to update record: {e}"
    elif method == "DELETE":
        message = f"Failed to delete record: {e}"
    else:
        message = f"Error: {e}"

    logger.error(message)
    raise HTTPException(
        status_code= status_code,
        detail={
            "status": "error",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
