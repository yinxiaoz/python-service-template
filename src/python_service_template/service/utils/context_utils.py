# Copyright (c) 2024, Flip Technology Corporation (Flip AI)

import logging
import uuid
from contextvars import ContextVar
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Context variables for request data
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
request_method_var: ContextVar[Optional[str]] = ContextVar("request_method", default=None)
request_url_var: ContextVar[Optional[str]] = ContextVar("request_url", default=None)
request_headers_var: ContextVar[Optional[Dict[str, Any]]] = ContextVar("request_headers", default=None)
request_query_args_var: ContextVar[Optional[Dict[str, Any]]] = ContextVar("request_query_args", default=None)


class RequestContext:
    @staticmethod
    def generate_request_id() -> str:
        """Generate a new request ID with 'req-' prefix"""
        return f"req-{str(uuid.uuid4())}"

    @staticmethod
    def set_request_id(request_id: str) -> None:
        """Set the request ID in the current context"""
        request_id_var.set(request_id)

    @staticmethod
    def get_request_id() -> str:
        """Get the request ID from the current context"""
        return request_id_var.get() or "None"

    @staticmethod
    def set_request_method(method: str) -> None:
        """Set the request method in the current context"""
        request_method_var.set(method)

    @staticmethod
    def get_request_method() -> str:
        """Get the request method from the current context"""
        return request_method_var.get() or "None"

    @staticmethod
    def set_request_url(url: str) -> None:
        """Set the request URL in the current context"""
        request_url_var.set(url)

    @staticmethod
    def get_request_url() -> str:
        """Get the request URL from the current context"""
        return request_url_var.get() or "None"

    @staticmethod
    def set_request_query_args(query_args: Dict[str, Any]) -> None:
        """Set the request query args in the current context"""
        request_query_args_var.set(query_args)

    @staticmethod
    def get_request_query_args() -> Dict[str, Any]:
        """Get the request query args from the current context"""
        return request_query_args_var.get() or {}

    @staticmethod
    def set_request_headers(headers: Dict[str, Any]) -> None:
        """Set the request headers in the current context"""
        request_headers_var.set(headers)

    @staticmethod
    def get_request_headers() -> Dict[str, Any]:
        """Get the request headers from the current context"""
        return request_headers_var.get() or {}
