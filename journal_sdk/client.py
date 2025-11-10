import logging
from datetime import date
from typing import Any, cast

from httpx import AsyncClient, Response

from journal_sdk.data import config
from journal_sdk.errors import journal_exceptions as _err
from journal_sdk.models.homework import Homeworks as _hw_model
from journal_sdk.models.schedule import Schedule as _sch_model
from journal_sdk.models.user_info import UserInfo as _uf_model
from journal_sdk.transport import Transport as _tp
from journal_sdk.utils.app_key import ApplicationKey as _ak


class Client:
    def __init__(self, client: AsyncClient, transport: Any | None = None) -> None:
        logging.getLogger(__name__).debug("Logging initialized.")

        self._client: AsyncClient = client
        self._transport: _tp = transport if transport else _tp(self._client)
        self._app_key: _ak = _ak()

    async def login(
        self, username: str, password: str, raw: bool | None = False
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
        strdate: str | date | None = None,
        raw: bool | None = False,
    ):
        if not strdate:  # Handle not provided date param
            logging.debug(f"date:{date}")
            logging.warning("Date not provided, using today date!")
            strdate = date.today()

        if token:
            _sch_response: Response = await self._transport.request(
                method="get",
                url=config.JournalEndpoint.SCHEDULE_URL.value,
                token=token,
                params={"date": str(strdate)},
            )

            logging.debug(f"Server respose: '{_sch_response.json()}'.")
            logging.info("Complite schedule data fetching.")

            if raw:
                return _sch_response.json()

            # Parse raw schedule data to object
            _schedule_object: _sch_model = _sch_model(lessons=_sch_response.json())

            logging.info("Complite schedule data parsing.")

            if _schedule_object:
                return _schedule_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")

        raise _err.InvalidJWTError()

    async def get_homework(
        self, token: str, raw: bool = False
    ) -> dict[int, int] | _hw_model | Any:
        if token:
            _hw_response: Response = await self._transport.request(
                method="get",
                url=config.JournalEndpoint.STUDENT_HOMEWORK.value,
                token=token,
            )

            logging.debug(f"Server respose: '{_hw_response.json()}'.")
            logging.info("Complite homework data fetching.")

            if raw:
                return _hw_response.json()

            _homework_object: _hw_model = _hw_model(counters=_hw_response.json())

            logging.info("Complite homework data parsing.")

            if _homework_object:
                return _homework_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")

        raise _err.InvalidJWTError()

    async def get_avg_score(self, token: str, raw: bool = False):
        if token:
            _score_response: Response = await self._transport.request(
                method="get", url=config.JournalEndpoint.METRIC_GRADE.value, token=token
            )

            logging.debug(f"Server respose: '{_score_response.json()}'.")
            logging.info("Complite avg score fetching.")

            if raw:
                return _score_response.json()

            # TODO!!!
            # _avg_score_object: Any = _uf_model(**_score_response.json())

            # logging.info("Complite user info parsing.")

            # if _avg_score_object:
            #     return _avg_score_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")
        raise _err.InvalidJWTError()

    async def get_user_info(self, token: str, raw: bool | None = False):
        if token:
            _inf_response: Response = await self._transport.request(
                method="get", url=config.JournalEndpoint.USER_INFO.value, token=token
            )

            logging.debug(f"Server respose: '{_inf_response.json()}'.")
            logging.info("Complite user info fetching.")

            if raw:
                return _inf_response.json()

            _user_info_object: Any = _uf_model(**_inf_response.json())

            logging.info("Complite user info parsing.")

            if _user_info_object:
                return _user_info_object

        logging.error("JWT Token not provided!")
        logging.debug(f"JWT: {token}")
        raise _err.InvalidJWTError()

    async def close_connection(self) -> None:
        """Close async connection with private client object"""
        await self._client.aclose()
        logging.info("Async connection closed!")

        return None
