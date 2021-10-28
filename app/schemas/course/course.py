from pydantic import BaseModel, Field

from typing import List

from app.schemas.course.lesson import Lesson, LessonBase


class CourseBase(BaseModel):
    title: str
    description: str
    type: str
    hashtags: str
    location: str
    lessons: List[LessonBase]


class CourseCreate(CourseBase):
    creator_id: str = Field(alias="user_id")


class CourseRegistration(BaseModel):
    user_id: str


class CourseCollaboration(BaseModel):
    user_id: str


class CourseUpdate(CourseBase):
    hashtags: str


# Properties shared by models stored in DB
class CourseInDBBase(CourseBase):
    id: int
    creator_id: str
    lessons: List[Lesson]

    class Config:
        orm_mode = True


# Properties to return to client
class Course(CourseInDBBase):
    pass


class CourseSearchResults(BaseModel):
    results: List[Course]
