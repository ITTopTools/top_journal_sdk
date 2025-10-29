from typing import final

from httpx import AsyncClient
from starlette.exceptions import HTTPException

from .data import config
from .transport import Transport
from .utils.app_key import ApplicationKey


@final
class Auth:
    def __init__(self, client: AsyncClient):
        self._app_key: ApplicationKey = ApplicationKey()
        self._transport: Transport = Transport(client)

    async def get_jwt_token(self, username: str, password: str) -> str:
        __auth_data = {
            "application_key": await self._app_key.get_key(True),
            "username": username,
            "password": password, 
            "id_city": None,
        }

        __request = await self._transport.request(
            method="post",
            url=config.AUTH_URL,
            json=__auth_data,
            timeout=2,
        )
        _jwt_token: str = __request.json()["access_token"]

        if _jwt_token:
            return _jwt_token
        else:
            raise HTTPException(403, "Invalid login data!")
