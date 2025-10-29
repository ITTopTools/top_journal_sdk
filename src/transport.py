import asyncio
import time
from typing import Any, final

import httpx

from .data import config
from .errors import errors
from .utils.app_key import ApplicationKey


@final
class Transport:
    def __init__(self, client: httpx.AsyncClient, refresh_callback = None) -> None:
        self._client: httpx.AsyncClient = client
        self._refresh_callback = refresh_callback

        self.headers: dict[str, str] = {
            "User-Agent": config.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": config.REFERER,
            "Origin": config.ORIGIN,
        }

    async def request(
        self,
        method: str,
        url: str,
        token: str | None = None,
        timeout: float = 5.0,
        **kwargs: Any,
    ) -> httpx.Response:
        async def _send() -> httpx.Response:  # wrapper - only request for re-use
            global headers
            headers = self.headers.copy()

            if token:
                headers["Authorization"] = f"Bearer {token}"

            return await self._client.request(
                method, url, headers=headers, **kwargs
            )

        start_time = time.time()

        while time.time() - start_time < timeout:
            global response
            response = await _send()

            if response.status_code == 403:
                raise errors.InvalidJWTError()

            elif response.status_code == 422:
                raise errors.JournalAuthError("Invalid login data!")

            elif response.status_code >= 500:
                raise errors.JournalInternalServerError(response.status_code)

            # Is ok, return result
            return response

        # If timeout is end
        raise errors.JournalRequestTimeoutError(408)
