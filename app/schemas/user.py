from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, validator, Field

from app.schemas.course.course import Course


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    birth_date: Optional[date]
    phone_type: Optional[str]
    phone_number: Optional[str]
    subscription: Optional[str] = "Base"


class UserDateValidation(UserBase):
    birth_date: Optional[date] = Field(None, example="10/02/1990")

    @validator("birth_date", pre=True)
    def parse_birth_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


# Properties to receive via API on creation
class UserCreate(UserDateValidation):
    email: EmailStr


class UserInDBBase(UserBase):
    user_id: str
    blocked: bool
    birth_date: date

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
class UserUpdate(UserDateValidation):
    subscription: Optional[str]
