from datetime import date
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.course.course import Course
from app.schemas.user import User


class EnrollCourseBase(BaseModel):
    active: bool
    current_lesson: Optional[int] = None
    grade: Optional[int] = None
    end_date: Optional[date] = None


# Properties to receive via API on creation
class EnrollCourseCreate(EnrollCourseBase):
    user_id: str
    course_id: int
    active: Optional[bool] = True


class EnrollCourseInDBBase(EnrollCourseBase):
    user: User
    course: Course
    start_date: date

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnrollCourse(EnrollCourseInDBBase):
    pass


class EnrollCourseBasics(EnrollCourseBase):
    start_date: date

    class Config:
        orm_mode = True


class EnrollCourseSearchResults(BaseModel):
    results: List[EnrollCourse]


# Properties to receive via API on update
class EnrollCourseUpdate(EnrollCourseBase):
    active: Optional[bool]
    current_lesson: Optional[int]
    grade: Optional[int]
    end_date: Optional[date]
