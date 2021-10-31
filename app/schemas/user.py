from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.course.course import Course


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    role: Optional[str]
    is_admin: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


class UserInDBBase(UserBase):
    user_id: str
    blocked: bool

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserSearchResults(BaseModel):
    results: List[User]


# Additional ...
class UserInDBCompleteBase(User):
    created_courses: List[Course]
    attending_courses: List[Course]
    collaborating_courses: List[Course]


# Properties to receive via API on update
class UserUpdate(BaseModel):
    ...
