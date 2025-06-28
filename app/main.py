from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Voice Transcriber Service")
app.include_router(router)
