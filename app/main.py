import logging.config
from os import path

from ddtrace import patch, tracer, config
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.common.error_handling import custom_request_validation_exception_handler

# setup loggers
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# Datadog
# Patch is here only for those who choose not to use `ddtrace-run`
patch(fastapi=True)

tracer.configure(
    hostname=settings.DATADOG_AGENT_HOST,
    port=8126,
    enabled=settings.DATADOG_TRACE_ENABLED
)

# Override service name
config.fastapi['service_name'] = settings.DD_SERVICE

app = FastAPI(title="Ubademy-back-py API", openapi_url="/openapi.json")

app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_exception_handler(
    RequestValidationError,
    custom_request_validation_exception_handler
)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    logger.info("Running server in debug mode")

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
