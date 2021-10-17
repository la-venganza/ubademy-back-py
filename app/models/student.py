from sqlalchemy import Column, ForeignKey, Table, Integer

from app.db.base_class import Base

student_table = Table('student', Base.metadata,
                      Column('user_id', ForeignKey('user_account.user_id'), primary_key=True),
                      Column('course_id', ForeignKey('course.id'), primary_key=True)
                      )
