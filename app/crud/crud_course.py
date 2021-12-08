from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, contains_eager
from sqlalchemy.sql.elements import or_

from app.crud.base import CRUDBase
from app.models.course.course import Course
from app.schemas.course.course import CourseCreate, CourseUpdate, Course as CoursePydantic, CourseType
from app.models.collaborator import Collaborator
from app.models.enroll_course import EnrollCourse
from app.models.enroll_course_exam import EnrollCourseExam
from app.schemas.subscription import SubscriptionTitle
from app.models.subscription import Subscription


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):

    def get_full_by_course_id(self, db: Session, *, course_id: str) -> Optional[Course]:
        return db.query(Course).options(joinedload('*')).filter(Course.id == course_id).first()

    # Be aware not to use this query to update anything. This query is forcing to bring only relations
    # from EnrollCourseExam with filter attributes, there might be missing information in course entity
    def get_exams_from_courses(self, db: Session, *, user_id: str, active_students: bool, graded: bool,
                               offset: int = 0, limit: int = 100) -> List[Course]:
        query = db.query(Course)\
            .outerjoin(Course.collaborators)\
            .join(Course.enrollments)
        if graded is not None:
            graded_filter = EnrollCourseExam.grade.is_not(None) if graded else EnrollCourseExam.grade.is_(None)
            query = query.join(EnrollCourse.exams).filter(graded_filter).options(contains_eager('enrollments.exams'))
        query = query.filter(or_(Course.creator_id == user_id, Collaborator.user_id == user_id))
        if active_students is not None:
            query = query.filter(EnrollCourse.active == active_students)
        query = query.offset(offset).limit(limit)
        return query.all()

    def get_courses_with_filters(self, db: Session, *, category_filter: CourseType, plan_filter: SubscriptionTitle,
                                 offset: int = 0, limit: int = 100) -> List[Course]:
        query = db.query(Course)
        if category_filter is not None:
            query = query.filter(func.lower(Course.type) == func.lower(category_filter.title()))
        if plan_filter is not None:
            query = query.join(Course.subscription_required)\
                .filter(func.lower(Subscription.title) == func.lower(plan_filter.title()))
        return query.offset(offset).limit(limit).all()

    def patch_course(
        self,
        db: Session,
        *,
        course_to_update: CourseUpdate,
        course_db_data: Course
    ) -> Course:
        pydantic_course_stored = CoursePydantic.from_orm(course_db_data)

        course_updates_data = course_to_update.dict(exclude_unset=True)

        # create the merged dict with new updates overwriting existing data
        updated_course_data = pydantic_course_stored.copy(update=course_updates_data)

        course_to_update_data = jsonable_encoder(updated_course_data, by_alias=False)
        course_to_update_db = self.model(**course_to_update_data)  # type: ignore
        db.merge(course_to_update_db)
        db.commit()
        db.refresh(course_db_data)
        return course_db_data

    ...


course = CRUDCourse(Course)
