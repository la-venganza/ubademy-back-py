from pydantic import BaseModel

from typing import List, Optional

from app.schemas.course.exam import ExamBase


class LessonBase(BaseModel):
    require: bool
    active: Optional[bool] = True
    sequence_number: int
    multimedia_id: str
    multimedia_type: str
    exam: Optional[ExamBase] = None

    class Config:
        orm_mode = True


class LessonCreate(LessonBase):
    course_id: int


class LessonUpdate(LessonBase):
    ...


# Properties shared by models stored in DB
class LessonInDBBase(LessonBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True


class Lesson(LessonInDBBase):
    pass


class LessonSearchResults(BaseModel):
    results: List[Lesson]
