from pydantic import BaseModel
from datetime import datetime

from typing import List, Optional

from app.schemas.course.question import QuestionBase, Question


class ExamBase(BaseModel):
    title: str
    description: str
    minimum_qualification: int
    questions: List[QuestionBase]

    class Config:
        orm_mode = True


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    minimum_qualification: Optional[int]
    questions: Optional[List[Question]]


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
