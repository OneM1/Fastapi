from datetime import datetime
import time
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, conint

class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
    
class pydanticPost(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: userOut

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title:str 
    content:str
    published:bool =True

class PostCreate(PostBase):
    pass
class PostUpdate(PostBase):
    pass
    
class PostResponse(pydanticPost):
    votes: int


class User(BaseModel):
    id:int
    email:str
    username:str
    created_at:datetime

class UserBase(BaseModel):
    email:EmailStr
    username:str
    password:str

class CreateUser(UserBase):
    pass

class UpdateUser(UserBase):
    pass
class DaleteUser(UserBase):
    pass
class UserResponse(User):
    pass

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str

class TokenData(BaseModel):
    id:Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1, ge=0)]