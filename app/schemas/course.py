from pydantic import BaseModel, Field

from typing import List


class CourseBase(BaseModel):
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
    creator_id: str = Field(alias="user_id")


class CourseRegistration(BaseModel):
    user_id: str


class CourseUpdate(CourseBase):
    subject: str


# Properties shared by models stored in DB
class CourseInDBBase(CourseBase):
    id: int
    creator_id: str

    class Config:
        orm_mode = True


# Properties to return to client
class Course(CourseInDBBase):
    pass


class CourseSearchResults(BaseModel):
    results: List[Course]
