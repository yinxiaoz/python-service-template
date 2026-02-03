"""FastAPI application entry point."""

import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config

from python_service_template.service.api.check_health_api import health_router
from python_service_template.service.middleware.request_logging import RequestLoggingMiddleware
from python_service_template.utils.logging_utils import configure_root_logger


def create_application() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(
        title="Python Service Template",
        description="A template for Python services",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(health_router)

    return app


async def main():

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    log_level = os.getenv("LOG_LEVEL", "INFO")

    configure_root_logger(getattr(logging, log_level.upper(), logging.INFO))
    logger = logging.getLogger(__name__)

    config = Config()
    config.bind = [f"{host}:{port}"]
    config.include_server_header = False

    app = create_application()

    logger.info(f"Starting server on {host}:{port}")

    await serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
