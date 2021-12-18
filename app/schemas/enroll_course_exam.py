from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.schemas.enroll_course import EnrollCourse, EnrollCourseBasics
from app.schemas.answer import Answer, AnswerBase, AnswerExamRQ, AnswerBasics, AnswerForStaff
from app.schemas.course.exam import Exam, ExamBase


class EnrollCourseExamBase(BaseModel):
    grade: Optional[int] = None
    answers: List[AnswerBase]


# Properties to receive via API on creation
class EnrollCourseExamCreate(EnrollCourseExamBase):
    enroll_course_id: int
    lesson_id: int
    exam_id: int


class EnrollCourseExamRQ(BaseModel):
    user_id: str
    answers: List[AnswerExamRQ]


class EnrollCourseExamGradingRQ(BaseModel):
    user_id: str
    exam_to_grade_id: int
    enroll_course_id: int
    grade: int = Field(..., ge=0, le=10, )


class EnrollCourseExamInDBBase(EnrollCourseExamBase):
    id: int
    enroll_course: EnrollCourse
    exam: Exam
    answers: List[Answer]
    exam_date: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnrollCourseExam(EnrollCourseExamBase):
    id: int
    enroll_course = EnrollCourseBasics
    answers: List[AnswerBasics]
    exam_date: datetime

    class Config:
        orm_mode = True


class EnrollCourseExamSearchResults(BaseModel):
    results: List[EnrollCourseExam]


class EnrollCourseExamForStaff(EnrollCourseExamBase):
    enroll_course_id: int
    exam: ExamBase
    answers: List[AnswerForStaff]
    exam_date: datetime

    class Config:
        orm_mode = True


# Properties to receive via API on update
class EnrollCourseExamUpdate(BaseModel):
    grade: Optional[int]
