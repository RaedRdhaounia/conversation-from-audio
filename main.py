from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.models.response import ResponseWrapper
from app.routes.transcription import transcription_router
from app.routes.healthcare import healthcare_router
from app.routes.root import root_router
from app.routes.summary import summary_router

app = FastAPI(title="Voice Transcriber Service")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(root_router)
app.include_router(healthcare_router)
app.include_router(transcription_router)
app.include_router(summary_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ResponseWrapper(
            status=422,
            success=False,
            message="Invalid request parameters.",
            data={"errors": exc.errors()},
        ).dict()
    )
