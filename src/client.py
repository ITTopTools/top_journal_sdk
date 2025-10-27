from httpx import AsyncClient

from .transport import Transport


class Client:
    def __init__(self, client: AsyncClient) -> None:
        # User AsyncClient object
        self._client: AsyncClient = client

        # Superstructure of httpx with auto-retry, refresh jwt and app_key
        self._transport: object = Transport()

    def login(self, username, password):
        pass

    def get_schedule(token: str, date: str):
        pass

    def get_homework(token: str, date: str):
        pass

    def close_connection(self):
        if self._client:  # FIXME - overkill?
            self._client.aclose()
            return
