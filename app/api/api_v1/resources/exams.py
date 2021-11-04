import logging

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app import deps, crud
from app.schemas.course.exam import Exam, ExamUpdateRq, ExamCreateRq
from app.models.course import Exam as ExamDb, Lesson
from app.services import course_service

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
