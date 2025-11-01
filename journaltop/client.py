import datetime
import logging
from typing import Any, Optional, cast

from httpx import AsyncClient, Response

from .data import config
from .errors import journal_exceptions
from .models.schedule import Schedule as sch_model
from .transport import Transport
from .utils.app_key import ApplicationKey

class Client:
    def __init__(self, client: AsyncClient) -> None:
        logging.getLogger(__name__).debug("Logging initialized.")

        self._client    : AsyncClient = client
        self._transport : Transport = Transport(self._client)
        self._app_key   : ApplicationKey = ApplicationKey()

    async def login(self, username: str, password: str) -> str:
        
        _auth_data = {
            "application_key": await self._app_key.get_key(True),
            "username": username,
            "password": password,
            "id_city": None,
        }

        _response: Response = await self._transport.request(
            method="post",
            url=config.JournalEndpoint.AUTH_URL.value,
            json=_auth_data,
            timeout=2.0,
        )

        _jwt_token: str = str(
            cast(dict[str, str], _response.json()).get("access_token", "")
        )

        if _jwt_token:
            return _jwt_token
        raise journal_exceptions.InvalidJWTError()

    async def get_schedule(
        self, token: str, date: Optional[str], timeout: Optional[float]
        ):
        if not date:
            logging.debug(f"date:{date}")
            logging.warning(f"Date not provided, using today date!; date:{date}")
        
        if token:
            _response: Response = await self._transport.request(
                method="get", 
                url=config.JournalEndpoint.SCHEDULE_URL.value,
                token=token,
                timeout=timeout if timeout else 2.0,
                params={"date": date if date else datetime.date.today()}
                )

            logging.debug(f"Server respose: '{_response.json()}'.")
            logging.info("Complite schedule data fetching.")

            schedule_object: Any = sch_model(lessons=_response.json())
            
            logging.info("Complite schedule data parsing.")

            if schedule_object:
                return schedule_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")
        raise journal_exceptions.InvalidJWTError()


    async def close_connection(self) -> None:
        await self._client.aclose()
        return
