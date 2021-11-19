from pydantic import BaseModel
from datetime import datetime

from typing import List, Optional

from app.schemas.course.question import QuestionBase, Question, QuestionUpdate


class ExamBase(BaseModel):
    title: str
    description: str
    minimum_qualification: int
    active: bool = False
    questions: List[QuestionBase]

    class Config:
        orm_mode = True


class ExamCreate(ExamBase):
    pass


class ExamUpdateBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    active: Optional[bool]
    minimum_qualification: Optional[int]
    questions: Optional[List[QuestionUpdate]]


class ExamUpdate(ExamUpdateBase):
    ...


class ExamUpdateFromLesson(ExamUpdateBase):
    id: Optional[int]


class ExamUpdateRq(BaseModel):
    user_id: str
    exam: ExamUpdate


class ExamCreateRq(BaseModel):
    user_id: str
    exam: ExamCreate


class ExamInDBBase(ExamBase):
    id: int
    creation_date: datetime
    questions: List[Question]

    class Config:
        orm_mode = True


# Properties to return to client
class Exam(ExamInDBBase):
    pass
