import httpx

from starlette.exceptions import HTTPException
from .transport import Transport
from .data import config


class Auth:
    def __init__(self, client):
        self.client: httpx.AsyncClient = client
        self._transport = Transport
        self.auth_headers = {
            "User-Agent": config.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": config.REFERER,
            "Origin": config.ORIGIN,
        }

    async def get_jwt_token(self, login: str, password: str) -> str:
        auth_data = {
            "application_key": config.APP_KEY,
            "username": f"{login}",
            "password": f"{password}",
            "id_city": None,
        }

        request = await self.client.get(
            config.AUTH_URL, params=auth_data, headers=self.auth_headers
        )
        requst = await self._transport.request("")
        request.raise_for_status()

        jwt_token = request.json()["access_token"]

        if jwt_token:
            return jwt_token

        raise HTTPException(401, "Invalid jwt token!")
