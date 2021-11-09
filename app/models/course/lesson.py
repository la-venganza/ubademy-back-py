from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class Lesson(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(256), nullable=True)
    require = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    sequence_number = Column(Integer, nullable=False)
    multimedia_id = Column(String(256), nullable=False)
    multimedia_type = Column(String(30), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete="CASCADE"))
    exam_id = Column(Integer, ForeignKey('exam.id'), nullable=True)
    exam = relationship(
        "Exam",
        uselist=False,
    )

    @auto_init()
    def __init__(self, **_):
        pass
