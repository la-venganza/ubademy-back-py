import logging

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from app import deps, crud
from app.schemas.course.exam import Exam, ExamUpdateRq, ExamCreateRq
from app.models.course import Exam as ExamDb, Lesson
from app.services import course_service
from app.schemas.enroll_course_exam import EnrollCourseExamCreate, EnrollCourseExamRQ, EnrollCourseExam, \
    EnrollCourseExamGradingRQ, EnrollCourseExamUpdate, EnrollCourseExamForStaff

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.post("/", status_code=status.HTTP_201_CREATED, response_model=Exam)
async def create_exam(course_id: int, lesson_id: int, exam_in: ExamCreateRq,
                      lesson: Lesson = Depends(course_service.get_lesson_by_id),
                      db: Session = Depends(deps.get_db),
                      ) -> dict:
    """
    Create an exam
    """
    await course_service.verify_course_with_creator(course_id=course_id, user_id=exam_in.user_id, db=db)
    if lesson.exam:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An exam already exists for lesson {lesson_id} and course {course_id}"
        )
    exam_db = crud.exam.create(db=db, obj_in=exam_in.exam)

    lesson.exam = exam_db
    crud.lesson.update_lesson(db=db, updated_lesson=lesson)

    return exam_db


@router_v1.get("/{exam_id}", status_code=status.HTTP_200_OK, response_model=Exam)
async def get(exam: ExamDb = Depends(course_service.get_exam_by_id), ) -> dict:
    """
    Get an exam from course and lesson, by id
    """
    return exam


@router_v1.patch("/{exam_id}", status_code=status.HTTP_200_OK, response_model=Exam)
async def update_exam(course_id: int, exam_update_rq: ExamUpdateRq,
                      exam: ExamDb = Depends(course_service.get_exam_by_id),
                      db: Session = Depends(deps.get_db), ) -> dict:
    """
    Update an exam by its creator, from course and lesson, by id
    """
    await course_service.verify_course_with_creator(course_id=course_id, user_id=exam_update_rq.user_id, db=db)

    exam_updated = crud.exam.patch_exam(
        db=db,
        exam_to_update=exam_update_rq.exam,
        exam_db_data=exam
    )

    return exam_updated


@router_v1.post("/{exam_id}/solution", status_code=status.HTTP_200_OK, response_model=EnrollCourseExam)
async def exam_answer(
        course_id: int, lesson_id: int, exam_id: int, exam_in: EnrollCourseExamRQ,
        exam: ExamDb = Depends(course_service.get_exam_by_id),
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Publish an exam for an enrolled student
    """
    user_id = exam_in.user_id
    enrollment = await course_service.get_user_enrollment(course_id=course_id, user_id=user_id, db=db)

    enroll_course_exam = crud.enroll_course_exam.create(
        db=db,
        obj_in=EnrollCourseExamCreate(
            enroll_course_id=enrollment.id, lesson_id=lesson_id, exam_id=exam_id, answers=exam_in.answers)
    )

    return enroll_course_exam


@router_v1.patch("/{exam_id}/solution", status_code=status.HTTP_200_OK, response_model=EnrollCourseExam)
async def exam_correction(
        course_id: int, lesson_id: int, exam_id: int, graded_exam_in: EnrollCourseExamGradingRQ,
        exam: ExamDb = Depends(course_service.get_exam_by_id),
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Publish grade for a student exam.
    """
    user_id = graded_exam_in.user_id
    exam_to_grade_id = graded_exam_in.exam_to_grade_id
    logger.info(f"Attempting to grade exam {exam_to_grade_id} by user {user_id} of course {course_id}")
    staff_verified = await course_service.verify_course_staff(course_id=course_id, user_id=user_id, db=db)
    if not staff_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Exams of course with id {course_id} can only be graded by it's creator or a collaborator"
        )
    enroll_course_exam = crud.enroll_course_exam.get(db=db, id=exam_to_grade_id)
    if not enroll_course_exam or \
            not (
                    enroll_course_exam.enroll_course_id == graded_exam_in.enroll_course_id
                    and enroll_course_exam.lesson_id == lesson_id and enroll_course_exam.exam_id == exam_id
            ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some information is invalid. There is no exam to grade for course_id {course_id},"
                   f" lesson_id {lesson_id}, exam_id {exam_id}, exam_to_grade_id {exam_to_grade_id}"
                   f" and enroll_course_exam_id {graded_exam_in.enroll_course_id}"
        )
    enroll_course_exam = crud.enroll_course_exam.update(
        db=db, db_obj=enroll_course_exam, obj_in=EnrollCourseExamUpdate(grade=graded_exam_in.grade))

    return enroll_course_exam


@router_v1.get("/{exam_id}/solution/{exam_taken_id}",
               status_code=status.HTTP_200_OK, response_model=EnrollCourseExamForStaff)
async def search_exam_publish_by_id(
    course_id: int, lesson_id: int, exam_id: int, exam_taken_id: int,
    user_id: str = Query(..., example="someUserId"),
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for exam by exam taken id for student to check the exam, or for course creator/collaborators.
    """
    enroll_course_exam = crud.enroll_course_exam.get(db=db, id=exam_taken_id)
    if not enroll_course_exam \
            or enroll_course_exam.enroll_course_id != course_id \
            or enroll_course_exam.lesson_id != lesson_id \
            or enroll_course_exam.exam_id != exam_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam taken with id {exam_taken_id} of course with id {course_id} and lesson id {lesson_id}"
                   f" and exam id {exam_id} was not found."
        )

    staff_verified = await course_service.verify_course_staff(course_id=course_id, user_id=user_id, db=db)
    student_verified = enroll_course_exam.enroll_course.user_id == user_id
    if not student_verified and not staff_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Exam of course with id {course_id} can only be seen by it's creator or a collaborator or by"
                   f" student owner"
        )
    return enroll_course_exam
