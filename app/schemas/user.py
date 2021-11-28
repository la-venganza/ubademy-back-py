from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.course.course import Course
from app.schemas.user_subscription import UserSubscriptionBasics, UserSubscriptionCreateBase


class UserBase(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    birth_date: Optional[date]
    phone_type: Optional[str]
    phone_number: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    subscriptions: List[UserSubscriptionCreateBase]


class UserCreateRQ(UserBase):
    email: EmailStr


class UserInDBBase(UserBase):
    user_id: str
    email: EmailStr
    blocked: bool
    is_admin: bool
    subscriptions: List[UserSubscriptionBasics]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserSearchResults(BaseModel):
    results: List[User]


class UserEnrollCourseInDBBase(BaseModel):
    active: bool
    current_lesson: Optional[int] = None
    grade: Optional[int] = None
    end_date: Optional[date] = None
    course: Course
    start_date: date

    class Config:
        orm_mode = True


# Additional ...
class UserInDBCompleteBase(User):
    created_courses: List[Course]
    enroll_courses: List[UserEnrollCourseInDBBase]
    collaborating_courses: List[Course]


# Properties to receive via API on update
class UserUpdate(UserBase):
    username: Optional[str]
