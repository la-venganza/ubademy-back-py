from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.course.course import Course


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    birth_date: Optional[date]
    phone_type: Optional[str]
    phone_number: Optional[str]
    subscription: Optional[str] = "Base"


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


class UserInDBBase(UserBase):
    user_id: str
    email: EmailStr
    blocked: bool
    is_admin: bool
    birth_date: Optional[date]

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
class UserUpdate(UserBase):
    subscription: Optional[str]
