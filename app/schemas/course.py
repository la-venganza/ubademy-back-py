from pydantic import BaseModel

from typing import Sequence


class CourseBase(BaseModel):
    id: int
    title: str
    length: int
    year: int
    teacher: str
    subject: str


class CourseCreate(CourseBase):
    title: str
    length: int
    year: int
    teacher: str
    subject: str


class CourseUpdate(CourseBase):
    subject: str


# Properties shared by models stored in DB
class CourseInDBBase(CourseBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Course(CourseInDBBase):
    pass


class CourseSearchResults(BaseModel):
    results: Sequence[Course]
