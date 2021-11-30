from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.course.choice import Choice
from app.schemas.course.question import Question


class AnswerBase(BaseModel):
    choice_id: Optional[int]
    text: Optional[str]


class AnswerCreate(AnswerBase):
    enroll_course_exam_id: int
    question_id: int


class AnswerExamRQ(AnswerBase):
    question_id: int
    text: Optional[str] = Field(alias="input_answer")


class AnswerInDBBase(AnswerBase):
    id: int
    enroll_course_exam_id: int
    question_id: int
    question: Question
    choice: Optional[Choice] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Answer(AnswerInDBBase):
    pass


class AnswerBasics(AnswerBase):
    id: int
    enroll_course_exam_id: int
    question_id: int

    class Config:
        orm_mode = True
