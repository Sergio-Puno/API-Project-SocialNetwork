from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    read_time: Optional[int] = None

# Schema for creating a post, validate user inputs
class PostCreate(PostBase):
    # TODO: Currently no adjustment from PostBase but we could add requirements specific to creating a post
    # such as a "scheduled_post" type thing where a time to go live is specified
    pass

# Schema for returning Posts to a user, restrict personal info
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

# Schema for creating a user, validate user inputs
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for returning User information to a user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

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
