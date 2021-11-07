from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.crud import user
from app.services import user_service


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await user_service.get_user_by_id(user_id="1", db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'The user with id 1 was not found'


@pytest.mark.asyncio
async def test_get_user_by_id_ok(user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    db_session = MagicMock()
    user_db = await user_service.get_user_by_id(user_id="1", db=db_session)
    assert user_db == user_complete_db
