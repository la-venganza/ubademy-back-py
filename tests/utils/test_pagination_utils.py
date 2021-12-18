import pytest
from fastapi import HTTPException

from app.utils import pagination_utils


@pytest.mark.asyncio
async def test_validate_pagination_invalid_page():
    with pytest.raises(HTTPException) as exception_response:
        await pagination_utils.validate_pagination(page=0, page_size=10)
    assert exception_response.value.status_code == 400
    assert str(exception_response.value.detail) == 'Page value must be at least 1'


@pytest.mark.asyncio
async def test_validate_pagination_invalid_page_size():
    with pytest.raises(HTTPException) as exception_response:
        await pagination_utils.validate_pagination(page=1, page_size=0)
    assert exception_response.value.status_code == 400
    assert str(exception_response.value.detail) == 'Page size must be at least 1'


def test_manual_pagination_chunks():
    values = range(10, 61)
    paginated_list = list(pagination_utils.manual_pagination_chunks(values, 10))
    assert len(paginated_list[0]) == 10
    assert len(paginated_list[1]) == 10
    assert len(paginated_list[2]) == 10
    assert len(paginated_list[3]) == 10
    assert len(paginated_list[4]) == 10
    assert len(paginated_list[5]) == 1
