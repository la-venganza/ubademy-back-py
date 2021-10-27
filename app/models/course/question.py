from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey('exam.id'))
    sequence_number = Column(Integer, nullable=False)
    type = Column(String(100), nullable=False)
    score = Column(Integer, nullable=False)
    multiple_choice = relationship(
        "MultipleChoiceQuestion",
        uselist=False
    )
    develop_question = relationship(
        "DevelopQuestion",
        uselist=False
    )
