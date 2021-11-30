import logging

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import crud
from app.models.course import Exam
from app.models.course import Lesson
from app.deps import get_db


async def get_course_by_id(course_id, db: Session = Depends(get_db)):
    course = crud.course.get(db=db, id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {course_id} was not found")
    return course


async def verify_course_with_creator(course_id: int, user_id: str, db: Session = Depends(get_db)):
    course = await get_course_by_id(course_id, db=db)
    if course.creator_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Course with id {course_id} can only be edited by it's creator"
        )
    return True


async def get_full_course_by_id(course_id, db: Session = Depends(get_db)):
    course = crud.course.get_full_by_course_id(db=db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {course_id} was not found")
    return course


async def get_lesson_by_id(db: Session = Depends(get_db), course_id: int = 0, lesson_id: int = 0) -> Lesson:
    logging.info(f"Getting lesson: {lesson_id}")
    course = await get_full_course_by_id(db=db, course_id=course_id)

    filtered_lessons = filter(lambda lesson_item: lesson_id == lesson_item.id, course.lessons)
    lesson = next(filtered_lessons, None)

    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The lesson with id {lesson_id} was not found")
    return lesson


async def get_exam_by_id(db: Session = Depends(get_db), course_id: int = 0,
                         lesson_id: int = 0, exam_id: int = 0) -> Exam:

    logging.info(f"Getting exam: {exam_id} from lesson: {lesson_id} and course {course_id}")

    lesson = await get_lesson_by_id(db=db, course_id=course_id, lesson_id=lesson_id)

    if lesson.exam is None or (lesson.exam.id != exam_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The exam with id {exam_id} was not found")

    return lesson.exam


async def get_user_enrollment(course_id: int, user_id: str, db: Session = Depends(get_db)):
    course = await get_course_by_id(course_id, db=db)

    filtered_enrollments = filter(lambda enrollment_item: user_id == enrollment_item.user_id, course.enrollments)
    enrollment = next(filtered_enrollments, None)

    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"The user with id {user_id} is not enrolled to course {course_id}")
    return enrollment
