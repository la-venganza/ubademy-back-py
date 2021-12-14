from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.services import course_service
from app.crud import course
from tests.helper.courses_helper import lesson_db_of_course_json, search_exams_response_json


@pytest.mark.asyncio
async def test_get_course_by_id_not_found(mocker):
    mocker.patch.object(course, 'get', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_course_by_id(course_id=1, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'Course with id 1 was not found'


@pytest.mark.asyncio
async def test_get_course_by_id_ok(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    course_from_db = await course_service.get_course_by_id(course_id=1, db=db_session)
    assert course_from_db == course_db


@pytest.mark.asyncio
async def test_verify_course_with_creator_course_not_found(mocker):
    mocker.patch.object(course, 'get', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.verify_course_with_creator(course_id=1, user_id="1", db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'Course with id 1 was not found'


@pytest.mark.asyncio
async def test_verify_course_with_creator_course_forbidden(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.verify_course_with_creator(course_id=1, user_id="2", db=db_session)
    assert exception_response.value.status_code == 403
    assert str(exception_response.value.detail) == 'Course with id 1 can only be edited by it\'s creator'


@pytest.mark.asyncio
async def test_verify_course_with_creator_course_ok(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    response = await course_service.verify_course_with_creator(course_id=1, user_id="1", db=db_session)
    assert response


@pytest.mark.asyncio
async def test_get_full_course_by_id_not_found(mocker):
    mocker.patch.object(course, 'get', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_full_course_by_id(course_id=1, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'Course with id 1 was not found'


@pytest.mark.asyncio
async def test_get_full_course_by_id_ok(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    course_from_db = await course_service.get_full_course_by_id(course_id=1, db=db_session)
    assert course_from_db == course_db


@pytest.mark.asyncio
async def test_get_lesson_by_id_course_not_found(mocker):
    mocker.patch.object(course, 'get', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_lesson_by_id(course_id=1, lesson_id=1, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'Course with id 1 was not found'


@pytest.mark.asyncio
async def test_get_lesson_by_id_id_lesson_not_found(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_lesson_by_id(course_id=1, lesson_id=2, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'The lesson with id 2 was not found'


@pytest.mark.asyncio
async def test_get_lesson_by_id_id_lesson_ok(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    lesson = await course_service.get_lesson_by_id(course_id=1, lesson_id=1, db=db_session)
    assert jsonable_encoder(lesson) == lesson_db_of_course_json


@pytest.mark.asyncio
async def test_get_exam_by_id_course_not_found(mocker):
    mocker.patch.object(course, 'get', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_exam_by_id(course_id=1, lesson_id=1, exam_id=1, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'Course with id 1 was not found'


@pytest.mark.asyncio
async def test_get_exam_by_id_lesson_not_found(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_exam_by_id(course_id=1, lesson_id=2, exam_id=1, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'The lesson with id 2 was not found'


@pytest.mark.asyncio
async def test_get_exam_by_id_exam_not_found(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await course_service.get_exam_by_id(course_id=1, lesson_id=1, exam_id=1, db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'The exam with id 1 was not found'


@pytest.mark.asyncio
async def test_get_exam_by_id_exam_ok(course_with_exam_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_with_exam_db)
    db_session = MagicMock()
    exam = await course_service.get_exam_by_id(course_id=1, lesson_id=2, exam_id=1, db=db_session)
    assert exam
    assert exam.title == "title"
    assert exam.description == "description"
    assert exam.minimum_qualification == 6


@pytest.mark.asyncio
async def test_get_exams_for_staff_empty(mocker):
    mocker.patch.object(course, 'get_exams_from_courses', return_value=[])
    db_session = MagicMock()
    exams = await course_service.get_exams_for_staff(
        staff_id="1", active_students_filter=True, graded_status_filter=True, db=db_session,
        pagination_limit=1, pagination_offset=1)
    assert exams == []


@pytest.mark.asyncio
async def test_get_exams_for_staff_ok(course_with_enrollments_with_exam_db, mocker):
    mocker.patch.object(course, 'get_exams_from_courses', return_value=[course_with_enrollments_with_exam_db])
    db_session = MagicMock()
    exams = await course_service.get_exams_for_staff(
        staff_id="1", active_students_filter=True, graded_status_filter=True, db=db_session,
        pagination_limit=1, pagination_offset=1)
    assert len(exams) == 1
    assert jsonable_encoder(exams) == [search_exams_response_json]


@pytest.mark.asyncio
async def test_verify_course_staff_false(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    verified = await course_service.verify_course_staff(user_id="2", course_id=1, db=db_session)
    assert not verified


@pytest.mark.asyncio
async def test_verify_course_staff_true(course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    db_session = MagicMock()
    verified = await course_service.verify_course_staff(user_id="1", course_id=1, db=db_session)
    assert verified
