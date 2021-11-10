import logging

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def custom_request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    body = jsonable_encoder(exc.body)
    errors = exc.errors()
    logging.info(f"Request: {body}")
    logging.info(f"Validation error: {errors}")
    return JSONResponse(content=jsonable_encoder({"detail": errors}),
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                        )
