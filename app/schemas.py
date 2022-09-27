from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    read_time: Optional[int] = None

class PostCreate(PostBase):
    pass

# Schema for returning Posts to a user
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# [UserLogin] Depricated in favor of FasAPI Oauth2UserRequestForm
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
