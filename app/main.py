from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request

from app.interface.dto.error_response import ErrorResponse
from app.interface.endpoints_v1 import router_v1
from app.interface.endpoints_v2 import router_v2
from app.interface.open_api import custom_openapi


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return ErrorResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail if isinstance(exc.detail, str) else "HTTP Error occurred",
            "code": exc.status_code,
            "errors": [str(exc.detail)] if isinstance(exc.detail, str) else []
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Format the list of errors as needed
    errors = [f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in exc.errors()]
    return ErrorResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "code": 422,
            "errors": errors
        },
    )


app.include_router(router_v1)
app.include_router(router_v2)
app.openapi_schema = custom_openapi(app=app)
