from datetime import date
import logging
from typing import Any, Optional, cast

from httpx import AsyncClient, Response

from .data import config
from .errors import journal_exceptions as _err
from .models.homework import Homeworks as _hw_model
from .models.schedule import Schedule as _sch_model
from .models.user_info import UserInfo as _uf_model
from .transport import Transport as _tp
from .utils.app_key import ApplicationKey as _ak


class Client:
    def __init__(self, client: AsyncClient) -> None:
        logging.getLogger(__name__).debug("Logging initialized.")

        self._client    : AsyncClient = client
        self._transport : _tp = _tp(self._client)
        self._app_key   : _ak = _ak()

    async def login(
        self, username: str, password: str, raw: Optional[bool] = False
        ) -> str:

        _auth_data = {
            "application_key": await self._app_key.get_key(True),
            "username": username,
            "password": password,
            "id_city": None,
        }

        _response: Response = await self._transport.request(
            method="post",
            url=config.JournalEndpoint.AUTH_URL.value,
            token=None, 
            json=_auth_data,
        )

        if raw:
            return _response.json()

        _jwt_token: str = str(
            cast(dict[str, str], _response.json()).get("access_token", "")
        )

        if _jwt_token:
            return _jwt_token
        raise _err.InvalidJWTError()


    async def get_schedule(
        self,
        token: str,  
        strdate: Optional[str | date] = None,
        raw: Optional[bool] = False 
        ):
        if not strdate: # Handle not provided date param
            logging.debug(f"date:{date}")
            logging.warning("Date not provided, using today date!")
            strdate = date.today() 
        
        if token:
            _sch_response: Response = await self._transport.request(
                method="get", 
                url=config.JournalEndpoint.SCHEDULE_URL.value,
                token=token,
                params={"date": strdate})

            logging.debug(f"Server respose: '{_sch_response.json()}'.")
            logging.info("Complite schedule data fetching.")
            
            if raw:
                return _sch_response.json()
            
            # Parse raw schedule data to object
            schedule_object: Any = _sch_model(lessons=_sch_response.json())
            
            logging.info("Complite schedule data parsing.")

            if schedule_object:
                return schedule_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")

        raise _err.InvalidJWTError()


    async def get_homework(self, token: str, raw: Optional[bool] = False):
        if token:
            _hw_response: Response = await self._transport.request(
                method="get", 
                url=config.JournalEndpoint.STUDENT_HOMEWORK.value,
                token=token)

            logging.debug(f"Server respose: '{_hw_response.json()}'.")
            logging.info("Complite homework data fetching.")
            
            if raw:
                return _hw_response.json()
                
            homework_object: Any = _hw_model(counters=_hw_response.json())
            
            logging.info("Complite homework data parsing.")

            if homework_object:
                return homework_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")

        raise _err.InvalidJWTError()
        

    async def get_avg_score(self, token: str, raw: Optional[bool] = False):
        if token: 
            _score_response: Response = await self._transport.request(
                method="get", 
                url=config.JournalEndpoint.METRIC_GRADE.value,
                token=token)

            logging.debug(f"Server respose: '{_score_response.json()}'.")
            logging.info("Complite avg score fetching.")
            
            if raw:
                return _score_response.json()
                
            # avg_score_object: Any = _uf_model(**_score_response.json())
            
            # logging.info("Complite user info parsing.")

            # if user_info_object:
            #     return user_info_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")
        raise _err.InvalidJWTError()


    async def get_user_info(self, token: str, raw: Optional[bool] = False):
        if token:
            _inf_response: Response = await self._transport.request(
                method="get", 
                url=config.JournalEndpoint.USER_INFO.value,
                token=token
                )

            logging.debug(f"Server respose: '{_inf_response.json()}'.")
            logging.info("Complite user info fetching.")
            
            if raw:
                return _inf_response.json()
                
            user_info_object: Any = _uf_model(**_inf_response.json())
            
            logging.info("Complite user info parsing.")

            if user_info_object:
                return user_info_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")
        raise _err.InvalidJWTError()


    async def close_connection(self) -> None:
        """Close async connection with private client object"""
        await self._client.aclose()
        logging.info("Async connection closed!")

        return None
