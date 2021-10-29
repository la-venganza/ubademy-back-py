from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete="CASCADE"))
    sequence_number = Column(Integer, nullable=False)
    type = Column(String(100), nullable=False)
    score = Column(Integer, nullable=False)
    multiple_choice_question = relationship(
        "MultipleChoiceQuestion",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )
    develop_question = relationship(
        "DevelopQuestion",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )

    @auto_init()
    def __init__(self, **_):
        pass
