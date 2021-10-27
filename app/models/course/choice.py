from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from app.db.base_class import Base


class Choice(Base):
    id = Column(Integer, primary_key=True, index=True)
    multiple_choice_question_id = Column(Integer, ForeignKey('multiplechoicequestion.id'))
    text = Column(String(256), nullable=False)
    is_correct = Column(Boolean, default=False)
