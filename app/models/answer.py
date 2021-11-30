from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class Answer(Base):
    id = Column(Integer, primary_key=True, index=True)
    enroll_course_exam_id = Column(Integer, ForeignKey('enroll_course_exam.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    choice_id = Column(Integer, ForeignKey('choice.id'))
    text = Column(String(500))
    question = relationship(
        "Question",
        uselist=False,
    )
    choice = relationship("Choice", uselist=False)

    @auto_init()
    def __init__(self, **_):
        pass
