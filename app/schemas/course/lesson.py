from pydantic import BaseModel

from typing import List, Optional

from app.schemas.course.exam import ExamBase, Exam, ExamUpdateFromLesson


class LessonBase(BaseModel):
    title: str
    description: Optional[str]
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
    exam: Optional[Exam] = None

    class Config:
        orm_mode = True


class LessonUpdate(LessonBase):
    id: Optional[int]
    exam: Optional[ExamUpdateFromLesson] = None

    class Config:
        orm_mode = True


class Lesson(LessonInDBBase):
    pass


class LessonSearchResults(BaseModel):
    results: List[Lesson]
