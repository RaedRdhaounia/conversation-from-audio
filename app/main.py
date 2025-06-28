from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="Voice Transcriber Service")
app.include_router(router)
