from fastapi import HTTPException, status


async def validate_pagination(page, page_size):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Page value must be at least 1")
    if page_size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Page size must be at least 1")


def manual_pagination_chunks(list_values, page_size):
    """Yield successive page-size chunks from list_values."""
    for i in range(0, len(list_values), page_size):
        yield list_values[i:i + page_size]
