from typing import Optional

from pydantic import BaseModel


class ChoiceBase(BaseModel):
    text: str
    is_correct: bool

    class Config:
        orm_mode = True


class ChoiceCreate(ChoiceBase):
    multiple_choice_question_id: int


class ChoiceUpdate(ChoiceBase):
    ...


class ChoiceInDBBase(ChoiceBase):
    id: int
    multiple_choice_question_id: int

    class Config:
        orm_mode = True


class ChoiceForStaff(ChoiceBase):
    pass


class ChoiceUpdate(ChoiceBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class Choice(ChoiceInDBBase):
    pass
