import logging
import time
from typing import Any, final

import httpx

from journal_sdk.data import config
from journal_sdk.errors import journal_exceptions

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
        method: str,
        url: str,
        token: str | None,
        timeout: float = 2.0,
        follow_redirects: bool = True,
        params: dict[str, Any] | None = None,
        json: dict[str, str | Any | None] | None = None,
    ) -> httpx.Response:
        async def _send() -> httpx.Response:
            global _headers

            _headers = self.headers.copy()

            if token:
                logging.debug("Sending request with token!")
                _headers["Authorization"] = f"Bearer {token}"

            else:
                logging.debug("Sending request without token!")

            return await self._client.request(
                method=method,
                url=url,
                headers=_headers,
                follow_redirects=follow_redirects,
                params=params,
                json=json,
            )

        __start_time: float = time.time()

        while time.time() - __start_time < timeout:
            logging.debug("Trying send request.")

            response = await _send()

            if response.status_code == 200:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                return response

            elif response.status_code == 401:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                raise journal_exceptions.OutdatedJWTError()

            elif response.status_code == 403:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                raise journal_exceptions.InvalidJWTError()

            elif response.status_code == 404:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                raise journal_exceptions.DataNotFoundError()

            elif response.status_code == 410:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                raise journal_exceptions.InvalidAppKeyError()

            elif response.status_code == 422:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                raise journal_exceptions.InvalidAuthDataError()

            elif response.status_code >= 500:
                logging.debug(
                    f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
                )
                raise journal_exceptions.InternalServerError(response.status_code)

            logging.debug(
                f"{response}; L{url}; H:{_headers}; T:{token}; P:{params}; J:{json} "
            )
        raise journal_exceptions.RequestTimeoutError()
