from typing import Any
from starlette.exceptions import HTTPException
from httpx import AsyncClient
from .data import config
from .transport import Transport


class Auth:
    def __init__(self, client: AsyncClient):
        self._transport: Transport = Transport(client)
        self.__auth_headers = {
            "User-Agent": config.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": config.REFERER,
            "Origin": config.ORIGIN,
        }

    async def get_jwt_token(self, login: str, password: str) -> str:
        __auth_data = {
            "application_key": config.APP_KEY,
            "username": f"{login}",
            "password": f"{password}",
            "id_city": None,
        }

        __request = await self._transport.request(
            method="get",
            url=config.AUTH_URL,
            headers=self.__auth_headers,
            params=__auth_data,
            timeout=2,
        )

        _jwt_token: str = __request.json()["access_token"]
        # refresh_token: str = __request.json()["refresh_token"] # for cache realisation, Dont remove!

        if _jwt_token:
            return _jwt_token
        else:
            raise HTTPException(403, "Invalid login data!")
