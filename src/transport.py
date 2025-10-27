import httpx
from .utils.app_key import appKey
from .data import config


class Transport:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client: httpx.AsyncClient = client
        self.app_key: object = appKey()

        self.default_headers = {
                        "User-Agent": config.USER_AGENT,
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "Referer": config.REFERER,
                        "Origin": config.ORIGIN
                    }

    async def request(self, token: str, method: str, url: str, **kwargs):

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.default_headers
        response = await self._client.request(method, url, headers=default_headers, **kwargs)

        if response.status_code in {401, 403}:
            await self.auth.refresh()
            return await self.request(method, url, **kwargs)

        elif response.status_code == 410:
            self.app_key.update()
            return await self.request(method, url, **kwargs)

        return response

        async def get_response_with_jwt(login: str, username: str):
