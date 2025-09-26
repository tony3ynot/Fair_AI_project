from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.api import api_router
import json

# Custom JSON encoder with proper UTF-8 handling
class UTF8JSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,  # Don't escape non-ASCII characters
            allow_nan=False,
            indent=None,
            separators=(",", ":")
        ).encode("utf-8")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redirect_slashes=False,  # Disable automatic trailing slash redirects
    default_response_class=UTF8JSONResponse  # Use custom response for proper UTF-8
)

# Set up CORS - MUST be before any route definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Use specific origins from settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to Fair AI API", "version": settings.VERSION}