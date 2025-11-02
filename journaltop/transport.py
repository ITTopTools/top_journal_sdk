import time
import logging
from typing import Any, final, Optional

import httpx

from .data import config
from .errors import journal_exceptions

logging.getLogger(__name__).info("Logging initialized")


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
        method  : str,
        url     : str,
        token   : Optional[str],
        follow_redirects: bool = True,
        timeout: float = 2.0,
        **kwargs: Optional[Any]
    ) -> httpx.Response:

        async def _send() -> httpx.Response: 
            _headers = self.headers.copy()

            if token:
                logging.info("Request with token!")
                _headers["Authorization"] = f"Bearer {token}"
            else:
                logging.info("Request without token!")

            return await self._client.request(
                method=method, 
                url=url, 
                headers=_headers, 
                follow_redirects=follow_redirects, 
                **kwargs
                )

        __start_time: float = time.time()

        while time.time() - __start_time < timeout:
            response = await _send()

            if response.status_code == 403 :
                raise journal_exceptions.InvalidJWTError()

            elif response.status_code == 401:
                raise journal_exceptions.OutdatedJWTError()
            
            elif response.status_code == 410:
                raise journal_exceptions.InvalidAppKeyError()

            elif response.status_code == 422:
                raise journal_exceptions.InvalidAuthDataError()

            elif response.status_code >= 500:
                raise journal_exceptions.InternalServerError(
                    response.status_code
                )

            return response

        raise journal_exceptions.RequestTimeoutError()
