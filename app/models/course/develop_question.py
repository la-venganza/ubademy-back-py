from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class DevelopQuestion(Base):
    __tablename__ = 'develop_question'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('question.id', ondelete="CASCADE"))
    text = Column(String(256), nullable=False)
