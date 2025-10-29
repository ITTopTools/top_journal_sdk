from httpx import AsyncClient

from .transport import Transport


class Client:
    def __init__(self, client: AsyncClient) -> None:
        # User AsyncClient object
        self._client: AsyncClient = client

        # Superstructure of httpx with auto-retry, refresh jwt and app_key
        self._transport: object = Transport(self._client)

    async def login(self, username: str, password: str):
        pass

    async def get_schedule(self, token: str, date: str):
        pass

    async def get_homework(self, token: str, date: str):
        pass

    async def close_connection(self):
        if self._client:  # FIXME - overkill?
            await self._client.aclose()
            return
