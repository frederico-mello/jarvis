from fastapi import Request, HTTPException, status
from src.config.settings import settings
from src.common.logging import get_logger
import time

logger = get_logger(__name__)


class RateLimiter:
    def __init__(self):
        self._requests: dict[str, list[float]] = {}

    async def check(self, request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = 60.0
        max_requests = settings.rate_limit_per_minute

        if client_ip not in self._requests:
            self._requests[client_ip] = []

        self._requests[client_ip] = [
            t for t in self._requests[client_ip]
            if now - t < window
        ]

        if len(self._requests[client_ip]) >= max_requests:
            logger.warning("Rate limit exceeded", client_ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
            )

        self._requests[client_ip].append(now)


rate_limiter = RateLimiter()
