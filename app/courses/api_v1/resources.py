import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.courses.schemas import CourseCreate, Course, CourseSearchResults
from app import deps
from app import crud
# from common.error_handling import ObjectNotFound

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/", status_code=200)
async def get():
    """""
       Get courses api
    """
    logging.info("Nonsense endpoint")
    return {"msg": "I'm a course"}


@router_v1.get("/search/", status_code=200, response_model=CourseSearchResults)
async def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="java"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for courses based on subject keyword
    """
    courses = crud.course.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": courses}

    results = filter(lambda course: keyword.lower() in course.subject.lower(), courses)
    return {"results": list(results)[:max_results]}


@router_v1.post("/", status_code=201, response_model=Course)
async def post(course_in: CourseCreate, db: Session = Depends(deps.get_db),) -> dict:

    course = crud.course.create(db=db, obj_in=course_in)

    return course


@router_v1.get("/{course_id}", status_code=200)
async def get(course_id: int, db: Session = Depends(deps.get_db), ):
    """""
    Get a single course by id
    """
    print(type(course_id))
    course = crud.course.get(db=db, id=course_id)

    if course is None:
        # raise ObjectNotFound('The course doesnt not exist')
        raise HTTPException(status_code=404, detail=f"The course with id {course_id} was not found")

    return course

