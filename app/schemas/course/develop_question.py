from pydantic import BaseModel


class DevelopQuestionBase(BaseModel):
    text: str


class DevelopQuestionCreate(DevelopQuestionBase):
    question_id: int


class DevelopQuestionUpdate(DevelopQuestionBase):
    ...


class DevelopQuestionInDBBase(DevelopQuestionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class DevelopQuestion(DevelopQuestionInDBBase):
    pass
