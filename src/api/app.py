from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.config.settings import settings
from src.common.logging import configure_logging, get_logger
from src.api.routes import router

logger = get_logger(__name__)


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        description="GraphRAG institucional do ICT-SJC UNESP",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup():
        logger.info("Application starting")

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Application shutting down")

    return app
