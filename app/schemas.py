from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Schema for returning User information to a user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Schema for creating a post, validate user inputs
class PostCreate(PostBase):
    # TODO: Currently no adjustment from PostBase but we could add requirements specific to creating a post
    # such as a "scheduled_post" type thing where a time to go live is specified
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True

# Schema for returning Posts to a user, restrict personal info
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# Schema for creating a user, validate user inputs
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for return login information upon successful user login
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Schema for voting, validate user input
class Vote(BaseModel):
    post_id : int
    dir: bool
