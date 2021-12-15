from typing import Optional

from pydantic import BaseModel

from app.schemas.course.develop_question import DevelopQuestionBase, DevelopQuestion, DevelopQuestionUpdate,\
    DevelopQuestionForStaff
from app.schemas.course.multiple_choice_question import MultipleChoiceQuestionBase, MultipleChoiceQuestion, \
    MultipleChoiceQuestionUpdate, MultipleChoiceQuestionForStaff


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


class QuestionInDBBase(QuestionBase):
    id: int
    exam_id: int
    multiple_choice_question: Optional[MultipleChoiceQuestion] = None
    develop_question: Optional[DevelopQuestion] = None

    class Config:
        orm_mode = True


class QuestionForStaff(QuestionBase):
    multiple_choice_question: Optional[MultipleChoiceQuestionForStaff] = None
    develop_question: Optional[DevelopQuestionForStaff] = None

    class Config:
        orm_mode = True


class QuestionUpdate(QuestionBase):
    id: Optional[int]
    multiple_choice_question: Optional[MultipleChoiceQuestionUpdate] = None
    develop_question: Optional[DevelopQuestionUpdate] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Question(QuestionInDBBase):
    pass
