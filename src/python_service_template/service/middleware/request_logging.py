# Copyright (c) 2024, Flip Technology Corporation (Flip AI)

import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from ..utils.context_utils import RequestContext

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request details and response times"""

    async def dispatch(self, request: Request, call_next):
        # Generate and set request ID
        request_id = request.headers.get("X-Request-Id") or RequestContext.generate_request_id()
        RequestContext.set_request_id(request_id)

        # Set other request context data
        RequestContext.set_request_method(request.method)
        RequestContext.set_request_url(str(request.url))
        RequestContext.set_request_headers(dict(request.headers))
        RequestContext.set_request_query_args(dict(request.query_params))

        start_time = time.time()

        # Skip logging for health check endpoints to reduce noise
        is_health_check = request.url.path in ["/health", "/readiness", "/liveness", "/ping"]

        if not is_health_check:
            logger.info(
                f"Request started: {request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "remote_addr": request.client.host if request.client else None,
                    "user_agent": request.headers.get("User-Agent", ""),
                    "request_id": request_id,
                },
            )

        try:
            response = await call_next(request)

            # Add request ID to response headers
            response.headers["X-Request-Id"] = request_id

            duration = (time.time() - start_time) * 1000

            if not is_health_check:
                logger.info(
                    f"Request completed: {request.method} {request.url.path} - {response.status_code} ({duration:.2f}ms)",
                    extra={
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_ms": f"{duration:.2f}ms",
                        "request_id": request_id,
                    },
                )

            return response
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"Request error: {request.method} {request.url.path} - Exception: {str(e)} ({duration:.2f}ms)",
                exc_info=True,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": f"{duration:.2f}ms",
                    "request_id": request_id,
                },
            )
            raise e
