from typing import List, Optional

from pydantic import BaseModel

from app.schemas.course.choice import ChoiceBase, Choice, ChoiceUpdate, ChoiceForStaff


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
    choices: List[Choice]

    class Config:
        orm_mode = True


class MultipleChoiceQuestionForStaff(MultipleChoiceQuestionBase):
    choices: List[ChoiceForStaff]

    class Config:
        orm_mode = True


class MultipleChoiceQuestionUpdate(MultipleChoiceQuestionBase):
    id: Optional[int]
    choices: List[ChoiceUpdate]

    class Config:
        orm_mode = True


# Properties to return to client
class MultipleChoiceQuestion(MultipleChoiceQuestionInDBBase):
    pass
