import logging

from fastapi import FastAPI

from app.courses.api_v1.api import course_router
from app.core.config import settings

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(title="Ubademy-back-py API", openapi_url="/openapi.json")

app.include_router(course_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    logger.info("Running server in debug mode")

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
