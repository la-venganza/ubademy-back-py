import logging
from os import path

from ddtrace import patch
from fastapi import FastAPI

from app.courses.api_v1.api import course_router
from app.core.config import settings

# setup loggers
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

patch(fastapi=True)
app = FastAPI(title="Ubademy-back-py API", openapi_url="/openapi.json")

app.include_router(course_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    logger.info("Running server in debug mode")

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
