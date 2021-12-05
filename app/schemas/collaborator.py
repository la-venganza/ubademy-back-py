from datetime import date
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.course.course import Course
from app.schemas.user import User


class CollaboratorBase(BaseModel):
    active: bool
    end_date: Optional[date] = None


# Properties to receive via API on creation
class CollaboratorCreate(CollaboratorBase):
    user_id: str
    course_id: int
    active: Optional[bool] = True


class CollaboratorInDBBase(CollaboratorBase):
    user: User
    course: Course
    start_date: date

    class Config:
        orm_mode = True


# Additional properties to return via API
class Collaborator(CollaboratorInDBBase):
    pass


class CollaboratorBasics(CollaboratorBase):
    start_date: date

    class Config:
        orm_mode = True


class CollaboratorSearchResults(BaseModel):
    results: List[Collaborator]


# Properties to receive via API on update
class CollaboratorUpdate(CollaboratorBase):
    active: Optional[bool]
    end_date: Optional[date]
