import time
from typing import Any, final

import httpx

from .data import config
from .errors import journal_exceptions


@final
class Transport:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client: httpx.AsyncClient = client

        self.headers: dict[str, str] = {
            "User-Agent": config.JournalHeaders.USER_AGENT.value,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": config.JournalHeaders.REFERER.value,
            "Origin": config.JournalHeaders.ORIGIN.value,
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

            return await self._client.request(method, url, headers=headers, **kwargs)

        start_time = time.time()

        while time.time() - start_time < timeout:
            global response
            response = await _send()

            if response.status_code == 403:
                raise journal_exceptions.InvalidJWTError()

            elif response.status_code == 422:
                raise journal_exceptions.JournalAuthError("Invalid login data!")

            elif response.status_code >= 500:
                raise journal_exceptions.JournalInternalServerError(response.status_code)

            # Is ok, return result
            return response

        # If timeout is end
        raise journal_exceptions.JournalRequestTimeoutError(408)
