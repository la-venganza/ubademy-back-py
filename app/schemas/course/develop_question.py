from typing import Optional

from pydantic import BaseModel


class DevelopQuestionBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class DevelopQuestionCreate(DevelopQuestionBase):
    question_id: int


class DevelopQuestionInDBBase(DevelopQuestionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


class DevelopQuestionForStaff(DevelopQuestionBase):
    pass


class DevelopQuestionUpdate(DevelopQuestionBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class DevelopQuestion(DevelopQuestionInDBBase):
    pass
