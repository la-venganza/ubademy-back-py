from pydantic import BaseModel, Field

from typing import List, Optional

from app.schemas.course.lesson import LessonBase, Lesson, LessonUpdate
from app.schemas.subscription import SubscriptionTitle, SubscriptionBasics


class CourseBase(BaseModel):
    title: str
    description: str
    type: str
    hashtags: str
    location: str
    lessons: List[LessonBase]
    subscription_id_required: int

    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    creator_id: str


class CourseCreateRQ(BaseModel):
    title: str
    description: str
    type: str
    hashtags: str
    location: str
    lessons: List[LessonBase]
    user_id: str
    subscription_required: Optional[str] = SubscriptionTitle.free


class CourseRegistration(BaseModel):
    user_id: str


class CourseCollaboration(BaseModel):
    user_id: str
    collaborator_id: str


class CourseUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    type: Optional[str]
    hashtags: Optional[str]
    location: Optional[str]
    lessons: Optional[List[LessonUpdate]]
    subscription_id_required: Optional[int] = Field(ge=1, le=3)

    class Config:
        orm_mode = True


class CourseUpdateRq(BaseModel):
    user_id: str
    course: CourseUpdate


# Properties shared by models stored in DB
class CourseInDBBase(CourseBase):
    id: int
    creator_id: str
    lessons: List[Lesson]
    subscription_required: SubscriptionBasics

    class Config:
        orm_mode = True


# Properties to return to client
class Course(CourseInDBBase):
    pass


class CourseSearchResults(BaseModel):
    results: List[Course]
