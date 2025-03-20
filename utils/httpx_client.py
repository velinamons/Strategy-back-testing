import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from settings import RETRY_ATTEMPTS, RETRY_MAX_WAIT, RETRY_MIN_WAIT, RETRY_MULTIPLIER, HTTPX_TIMEOUT

client = httpx.AsyncClient(timeout=HTTPX_TIMEOUT)

retry_on_httpx = retry(
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=RETRY_MULTIPLIER, min=RETRY_MIN_WAIT, max=RETRY_MAX_WAIT
    ),
    retry=retry_if_exception_type(
        (httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException)
    ),
)
