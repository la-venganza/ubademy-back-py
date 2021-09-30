from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    length = Column(String(256), nullable=False)
    year = Column(Integer, nullable=False)
    teacher = Column(String(256), nullable=False)
    subject = Column(String(256), index=True, nullable=False)