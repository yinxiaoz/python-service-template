# Copyright (c) 2024, Flip Technology Corporation (Flip AI)


import logging
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel
from pythonjsonlogger import jsonlogger

from python_service_template.service.utils.context_utils import RequestContext


class RequestLogFilter(logging.Filter):
    """
    Log filter to inject the current request id of the request under `log_record.request_id`
    """

    def filter(self, log_record):
        log_record.request_id = RequestContext.get_request_id()
        return log_record


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        log_record["function"] = f"{record.name}:{record.lineno}"
        # log_record["func"] = record.funcName
        log_record["proc"] = record.processName
        log_record["thrd"] = record.threadName

        # Handle exception info in a more compact way
        if record.exc_info:
            import traceback

            # Get just the exception type and message, not the full stack trace
            exc_type, exc_value, exc_traceback = record.exc_info
            log_record["exception_type"] = exc_type.__name__ if exc_type else None
            log_record["exception_message"] = str(exc_value) if exc_value else None
            # Only include the last few frames of the stack trace to keep it manageable
            if exc_traceback:
                tb_lines = traceback.format_tb(exc_traceback)
                # Take only the last 3 frames to keep the log size down
                log_record["exception_stack"] = "".join(tb_lines[-3:]).strip()

        # Remove the default exc_info field which contains the full stack trace
        if "exc_info" in log_record:
            del log_record["exc_info"]

        # log_record["request_context"] = {
        #     "rquest_url": RequestContext.get_request_url(),
        #     "request_method": RequestContext.get_request_method(),
        #     "request_headers": RequestContext.get_request_headers(),
        #     "request_query_args": RequestContext.get_request_query_args(),
        # }


def json_translate(obj: Any):
    if isinstance(obj, BaseModel):
        return obj.model_dump()


def configure_root_logger(level: int = logging.INFO) -> None:
    """Default root logger for the service, all module level loggers will inherit the root logger handler if not overridden

    Args:
        level (int, optional): _description_. Defaults to logging.INFO.

    Returns:
        None: _description_
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    error_only_libs = [
        "boto3",
        "botocore",
        "urllib3",
        "pynamodb",
        "httpcore",
        "httpx",
        "datadog",
        "numba",
        "aiohttp",
        "drain3",
        "sklearn",
        "asyncio",
        "prisma",
        "ddtrace",
        "opentelemetry",
    ]
    for error_only_lib in error_only_libs:
        logging.getLogger(error_only_lib).setLevel(logging.ERROR)

    # fmt_str = "%(timestamp)s %(level)s %(proc)d %(thrd)s %(module_and_lineno)s %(func)s %(request_id)s %(message)s"
    # fmt_str = "%(timestamp)s %(level)s %(proc)d %(thrd)s %(request_id)s %(request_method)s %(request_url)s %(request_headers)s %(request_query_args)s %(message)s"
    # fmt_str = "%(timestamp)s %(level)s %(proc)d %(thrd)s %(request_id)s %(request_context)s %(message)s"
    fmt_str = "%(timestamp)s %(level)s %(proc)d %(thrd)s %(request_id)s %(function)s %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%SZ"

    log_formatter = logging.Formatter(fmt=fmt_str, datefmt=fmt_str)
    log_formatter = jsonlogger.JsonFormatter(fmt=fmt_str, datefmt=fmt_str)
    log_formatter = CustomJsonFormatter(fmt=fmt_str, datefmt=datefmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.addFilter(RequestLogFilter())

    for _h in root_logger.handlers:
        # if this function is invoked twice - then we do not want each log to be logged N times [N being number of times this function was called]
        root_logger.removeHandler(hdlr=_h)
    root_logger.addHandler(console_handler)
