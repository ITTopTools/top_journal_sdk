import httpx
from .utils.app_key import appKey
from .data import config
from starlette import HTTPexception

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
            token: str | None = None, # optional token argument 
            **kwargs
            ):

        if token:
            self.headers["Authorization"] = f"Bearer {token}"

        self.default_headers
        response = await self._client.request(method, url, headers=self.headers, **kwargs)

        if response.status_code in {401, 403}:
            await self.auth.refresh()
            return await self.request(method, url, **kwargs)

        elif response.status_code == 410:
            self.app_key.update()
            return await self.request(method, url, **kwargs)
        
        elif response.status_code >=500:
            raise HTTPexception()

        return response
