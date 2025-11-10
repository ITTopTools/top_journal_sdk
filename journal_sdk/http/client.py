from typing import Any

import httpx

from journal_sdk.enums.headers import JournalHeaders
from journal_sdk.http import exceptions


class HttpClient:
    def __init__(self) -> None:
        self.client: httpx.AsyncClient = httpx.AsyncClient()
        self.headers: dict[str, str] = {
            "User-Agent": JournalHeaders.USER_AGENT.value,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": JournalHeaders.REFERER.value,
            "Origin": JournalHeaders.ORIGIN.value,
        }
        self.client.headers.update(self.headers)

    async def _handle_response(self, response: httpx.Response):
        if response.status_code == 200:
            return response

        elif response.status_code == 401:
            raise exceptions.OutdatedJWTError()

        elif response.status_code == 403:
            raise exceptions.InvalidJWTError()

        elif response.status_code == 404:
            raise exceptions.DataNotFoundError()

        elif response.status_code == 410:
            raise exceptions.InvalidAppKeyError()

        elif response.status_code == 422:
            raise exceptions.InvalidAuthDataError()

        elif response.status_code >= 500:
            raise exceptions.InternalServerError(response.status_code)

    async def request(
        self,
        method: str,
        url: str,
        token: str | None = None,
        timeout: float = 2.0,
        follow_redirects: bool = True,
        params: dict[str, Any] | None = None,
        json: dict[str, str | Any | None] | None = None,
    ) -> httpx.Response | None:
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
            self.client.headers.update(self.headers)
        response = await self.client.request(
            method=method,
            url=url,
            headers=self.headers,
            follow_redirects=follow_redirects,
            params=params,
            json=json,
            timeout=timeout,
        )
        return await self._handle_response(response)

        # raise exceptions.RequestTimeoutError()

    async def get(self, endpoint: str, params: dict[str, Any]):
        return await self.request(method="GET", url=endpoint, params=params)
