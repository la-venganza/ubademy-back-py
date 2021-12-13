from pydantic import BaseModel, Field, validator
from aenum import Enum

from typing import List, Optional

from app.schemas.course.lesson import LessonBase, Lesson, LessonUpdate
from app.schemas.subscription import SubscriptionTitle, SubscriptionBasics


class CourseType(str, Enum):
    programming = "Programming"
    music = "Music"
    cooking = "Cooking"
    mindfulness = "Mindfulness"
    economy = "Economy"
    art = "Art"
    language = "Language"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def _missing_value_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member

    @classmethod
    def _missing_name_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member


class CourseTypeResults(BaseModel):
    course_types: List[str]


class CourseBase(BaseModel):
    title: str
    description: str
    type: CourseType
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
    type: CourseType
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
    type: Optional[CourseType]
    hashtags: Optional[str]
    location: Optional[str]
    lessons: Optional[List[LessonUpdate]]
    subscription_id_required: Optional[int] = Field(ge=1, le=10)

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


class CourseBasics(BaseModel):
    id: int
    title: str
    description: str
    type: CourseType
    hashtags: str
    location: str
    subscription_required_: str = Field(..., alias="subscription_required")
    creator_id: str
    creator_: str = Field(..., alias="creator")

    class Config:
        orm_mode = True

    @validator('subscription_required_', always=True, pre=True)
    def validate_subscription_required_title(cls, v):
        if v is None:
            raise TypeError('"subscription_required" is None')
        if isinstance(v, str):
            return v
        if v.title is None:
            raise ValueError('Not found "title" in "subscription_required"')
        return v.title

    @validator('creator_', always=True, pre=True)
    def validate_creator_username(cls, v):
        if v is None:
            raise TypeError('"creator" is None')
        if isinstance(v, str):
            return v
        if v.username is None:
            raise ValueError('Not found "username" in "creator"')
        return v.username
