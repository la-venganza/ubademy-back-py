from typing import List

from pydantic import BaseModel

from schemas.course.choice import Choice, ChoiceBase


class MultipleChoiceQuestionBase(BaseModel):
    text: str
    amount_of_options: int
    choices: List[ChoiceBase]


class MultipleChoiceQuestionCreate(MultipleChoiceQuestionBase):
    question_id: int


class MultipleChoiceQuestionUpdate(MultipleChoiceQuestionBase):
    ...


class MultipleChoiceQuestionInDBBase(MultipleChoiceQuestionBase):
    id: int
    question_id: int
    choices: List[Choice]

    class Config:
        orm_mode = True


# Properties to return to client
class MultipleChoiceQuestion(MultipleChoiceQuestionInDBBase):
    pass
