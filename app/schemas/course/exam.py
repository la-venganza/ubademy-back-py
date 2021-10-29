from pydantic import BaseModel
from datetime import datetime

from typing import List

from app.schemas.course.question import Question, QuestionBase


class ExamBase(BaseModel):
    title: str
    description: str
    minimum_qualification: int
    questions: List[QuestionBase]


class ExamCreate(ExamBase):
    lesson_id: int


class ExamUpdate(ExamBase):
    ...


class ExamInDBBase(ExamBase):
    id: int
    creation_date: datetime
    questions: List[Question]

    class Config:
        orm_mode = True


# Properties to return to client
class Exam(ExamInDBBase):
    pass