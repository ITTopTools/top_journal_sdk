from httpx import AsyncClient, Response
from typing import cast 


from .transport import Transport
from .data import config 
from .utils.app_key import ApplicationKey

class Client:
    def __init__(self, client: AsyncClient) -> None:
        self._client    : AsyncClient = client
        self._transport : Transport = Transport(self._client)
        self._app_key   : ApplicationKey = ApplicationKey()

    async def login(self, username: str, password: str):
        _auth_data = {
            "application_key": await self._app_key.get_key(True),
            "username": username,
            "password": password,
            "id_city": None,
        }

        _response: Response = await self._transport.request(
            method="post",
            url=config.AUTH_URL,
            json=_auth_data,
            timeout=2.0,
        )

        _jwt_token: str = str(
            cast(dict[str, str], _response.json()).get("access_token", "")
        )

        if _jwt_token:
            return _jwt_token

    async def get_schedule(self, token: str, date: str):
        pass

    async def get_homework(self, token: str, date: str):
        pass

    async def close_connection(self):
        await self._client.aclose()
        return
