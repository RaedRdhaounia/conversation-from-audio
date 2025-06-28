"""
app/routes/root.py

Defines the root ("/") endpoint for basic server confirmation.
"""

from fastapi import APIRouter
from app.models.response import ResponseWrapper

root_router = APIRouter()

@root_router.get(
    "/",
    summary="Root Endpoint",
    response_description="Returns a message indicating the server is running.",
    response_model=ResponseWrapper
)
async def root_status():
    """
    Returns a success message to confirm the API server is up and accessible.

    This can be used as a simple heartbeat or greeting endpoint.

    Returns:
        ResponseWrapper: Standard response with server status.
    """
    return ResponseWrapper(
        status=200,
        success=True,
        message="Server is running successfully.",
        data={"status": "running"}
    )
