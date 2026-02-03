# Copyright (c) 2024, Flip Technology Corporation (Flip AI)

import logging
from typing import Dict

from fastapi import APIRouter

logger = logging.getLogger(__name__)

health_router = APIRouter()


@health_router.get("/health")
async def check_health() -> Dict[str, str]:
    """Health check endpoint"""
    # Suppress logging for health checks to reduce noise
    res_payload = {"status": "ok"}
    return res_payload
