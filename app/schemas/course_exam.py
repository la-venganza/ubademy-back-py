from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class CourseExam(BaseModel):
    course_id: int
    course_title: str
    student_id: str
    student_email: EmailStr
    active_student: bool
    exam_taken_id: int
    exam_date: datetime
    exam_grade: Optional[int]
    enroll_course_id: int
    lesson_id: int
    exam_id: int


class CourseExamResults(BaseModel):
    results: List[CourseExam]
