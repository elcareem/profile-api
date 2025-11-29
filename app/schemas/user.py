from pydantic import BaseModel, Field, EmailStr, validator, model_validator
from typing import Optional
import re

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    image_url: Optional[str]

class UserCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str

    @validator('name')
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty or only spaces")

        if not re.search(r"[A-Za-z' ]+", value):
            raise ValueError("Name contains invalid characters")

        return value
    
    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain atleast one capital letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain atleast one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('password must contain atleast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain atleast one special character')
        return value
    
    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None