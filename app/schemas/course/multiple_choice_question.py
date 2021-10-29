from typing import List

from pydantic import BaseModel

from schemas.course.choice import ChoiceBase


class MultipleChoiceQuestionBase(BaseModel):
    text: str
    amount_of_options: int
    choices: List[ChoiceBase]

    class Config:
        orm_mode = True


class MultipleChoiceQuestionCreate(MultipleChoiceQuestionBase):
    question_id: int


class MultipleChoiceQuestionUpdate(MultipleChoiceQuestionBase):
    ...


class MultipleChoiceQuestionInDBBase(MultipleChoiceQuestionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class MultipleChoiceQuestion(MultipleChoiceQuestionInDBBase):
    pass
