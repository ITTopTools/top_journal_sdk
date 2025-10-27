import asyncio
import time

import httpx

from .data import config
from .errors import errors
from .utils.app_key import appKey


class Transport:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client: httpx.AsyncClient = client
        
        self.app_key: object = appKey()
        
        self.headers = {
                        "User-Agent": config.USER_AGENT,
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "Referer": config.REFERER,
                        "Origin": config.ORIGIN
                    }

    async def request(
            self, method: str, url: str, 
            token: str | None = None, 
            timeout: float = 5.0, 
            **kwargs
        ) -> httpx.Response:

        # wrapper - only request for re-use 
        async def _send():
            
            headers = self.headers.copy()

            if token:
                headers["Authorization"] = f"Bearer {token}"

            return await self.__client.request(
                method, url, headers=headers, **kwargs)

        start_time = time.time()

        while time.time() - start_time < timeout:
            response = await _send()

            if response.status_code in {401, 403}:
                await asyncio.sleep(1)
                await self.auth.refresh()
                continue

            elif response.status_code == 410:
                await asyncio.sleep(1)
                self.app_key.update()
                continue

            elif response.status_code >= 500:
                raise errors.JournalInternalServerError(response.status_code)

            # Is ok, return result
            return response

        # If timeout 
        raise errors.RequestTimeoutError("Retry timeout exceeded")
