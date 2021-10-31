from typing import Optional

from pydantic import BaseModel

from app.schemas.course.develop_question import DevelopQuestionBase
from app.schemas.course.multiple_choice_question import MultipleChoiceQuestionBase


class QuestionBase(BaseModel):
    sequence_number: int
    type: str
    score: int
    multiple_choice_question: Optional[MultipleChoiceQuestionBase] = None
    develop_question: Optional[DevelopQuestionBase] = None

    class Config:
        orm_mode = True


class QuestionCreate(QuestionBase):
    exam_id: int


class QuestionUpdate(QuestionBase):
    ...


class QuestionInDBBase(QuestionBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Question(QuestionInDBBase):
    pass
