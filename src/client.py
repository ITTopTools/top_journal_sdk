from httpx import AsyncClient

from .transport import Transport
from .auth import Auth


class Client:
    def __init__(self, client: AsyncClient) -> None:
        self._client: AsyncClient = client
        self._auth: Auth = Auth(self._client)
        self._transport: Transport = Transport(self._client)

    async def login(self, username: str, password: str) -> str:
        return await self._auth.get_jwt_token(username, password)

    async def get_schedule(self, token: str, date: str):
        pass

    async def get_homework(self, token: str, date: str):
        pass

    async def close_connection(self):
        if self._client:
            await self._client.aclose()
            return
