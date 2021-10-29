from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class Lesson(Base):
    id = Column(Integer, primary_key=True, index=True)
    require = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    sequence_number = Column(Integer, nullable=False)
    multimedia_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))
    exam_id = Column(Integer, ForeignKey('exam.id'), nullable=True)
    exam = relationship(
        "Exam",
        uselist=False,
    )

    @auto_init()
    def __init__(self, **_):
        pass
