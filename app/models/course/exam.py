from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class Exam(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(256), nullable=False)
    minimum_qualification = Column(Integer, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    questions = relationship("Question")
    # TODO This is temporarily here, just if we decide that we want to create an exam separate from a lesson
    lesson = relationship("Lesson", back_populates="exam")

    @auto_init()
    def __init__(self, **_):
        pass
