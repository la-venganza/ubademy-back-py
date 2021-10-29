from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class MultipleChoiceQuestion(Base):
    __tablename__ = 'multiple_choice_question'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('question.id', ondelete="CASCADE"))
    text = Column(String(256), nullable=False)
    amount_of_options = Column(Integer, nullable=False, default=2)
    choices = relationship(
        "Choice",
        cascade="all, delete",
        passive_deletes=True
    )

    @auto_init()
    def __init__(self, **_):
        pass
