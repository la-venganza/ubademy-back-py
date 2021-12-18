import logging

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import crud
from app.models.course import Exam
from app.models.course import Lesson
from app.deps import get_db
from app.schemas.course_exam import CourseExam, ExamBasics
from app.utils import pagination_utils


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


async def get_lesson_by_id(db: Session = Depends(get_db), course_id: int = 0, lesson_id: int = 0) -> Lesson:
    logging.info(f"Getting lesson: {lesson_id}")
    course = await get_course_by_id(db=db, course_id=course_id)

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


async def get_exams_for_staff(staff_id: str, active_students_filter: bool, graded_status_filter: bool,
                              pagination_limit: int, pagination_offset: int, db: Session = Depends(get_db)):
    courses = crud.course.get_exams_from_courses(
        db=db, user_id=staff_id, active_students=active_students_filter, graded=graded_status_filter,
        offset=pagination_offset, limit=pagination_limit
    )
    exams = []
    for course in courses:
        for enrollment in course.enrollments:
            for enroll_course_exam in enrollment.exams:
                exam = CourseExam(
                        course_id=course.id,
                        course_title=course.title,
                        student_id=enrollment.user_id,
                        student_email=enrollment.user.email,
                        student_username=enrollment.user.username,
                        exam_taken_id=enroll_course_exam.id,
                        lesson_id=enroll_course_exam.lesson_id,
                        exam_id=enroll_course_exam.exam_id,
                        exam_date=enroll_course_exam.exam_date,
                        active_student=enrollment.active,
                        exam_grade=enroll_course_exam.grade,
                        enroll_course_id=enroll_course_exam.enroll_course_id
                    )
                exams.append(exam)
    return exams


async def get_course_exams_for_staff(staff_id: str, course_id: int, pagination_limit: int, pagination_offset: int,
                                     db: Session = Depends(get_db)):
    course = await get_course_for_staff(course_id=course_id, user_id=staff_id, db=db)

    exams = []
    for lesson in course.lessons:
        if lesson.exam:
            exam = lesson.exam
            exam_basics = ExamBasics(
                course_id=course.id,
                lesson_id=lesson.id,
                id=exam.id,
                title=exam.title,
                description=exam.description,
                minimum_qualification=exam.minimum_qualification,
                active=exam.active
            )
            exams.append(exam_basics)
    paginated_exams = list(pagination_utils.manual_pagination_chunks(exams, pagination_limit))
    if len(paginated_exams) <= pagination_offset:
        return []
    return paginated_exams[pagination_offset]


async def verify_course_staff(course_id: int, user_id: str, db: Session = Depends(get_db)):
    course = await get_course_by_id(course_id, db=db)
    if course.creator_id == user_id or any(collaborator.user_id == user_id for collaborator in course.collaborators):
        return True
    return False


async def get_course_for_staff(course_id: int, user_id: str, db: Session = Depends(get_db)):
    course = await get_course_by_id(course_id, db=db)
    staff_verified = True if \
        (course.creator_id == user_id or any(collaborator.user_id == user_id for collaborator in course.collaborators))\
        else False
    if not staff_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Exams of course with id {course_id} can only be listed for it's creator or a collaborator"
        )
    return course
