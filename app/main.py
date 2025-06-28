"""
main.py

FastAPI entry point for the Voice Transcriber Service.
Includes routing and a global exception handler for request validation errors.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.models.response import ResponseWrapper
from app.routes.routes import router
from app.routes.healthcare import healthcare_router 
from app.routes.root import root_router

app = FastAPI(title="Voice Transcriber Service")

app.include_router(root_router)
app.include_router(healthcare_router)
app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles validation errors raised when request body/query/params don't match the expected schema.

    Args:
        request (Request): The incoming FastAPI request object.
        exc (RequestValidationError): The exception raised when validation fails.

    Returns:
        JSONResponse: A standardized error response with status, success, message, and details of the validation errors.
    """
    return JSONResponse(
        status_code=422,
        content=ResponseWrapper(
            status=422,
            success=False,
            message="Invalid request parameters.",
            data={"errors": exc.errors()},
        ).dict()
    )
