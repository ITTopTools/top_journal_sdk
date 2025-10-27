
from starlette.exceptions import HTTPException

from .data import config
from .transport import Transport


class Auth:
    def __init__(self):
        self.__transport = Transport
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

        _request = await self.__transport.request("get", config.AUTH_URL, 
            params=__auth_data, 
            headers=self.__auth_headers
        )

        _jwt_token = _request.json()["access_token"]

        if _jwt_token:
            return _jwt_token
        else:
            raise HTTPException(403, "Invalid login data!")
