from datetime import date
from typing import Any, cast

from httpx import AsyncClient, Response

from journal_sdk.enums.endpoints import JournalEndpoints
from journal_sdk.http import exceptions
from journal_sdk.http.client import HttpClient
from journal_sdk.models.homework import Homeworks as _hw_model
from journal_sdk.models.schedule import Schedule as _sch_model
from journal_sdk.models.user_info import UserInfo as _uf_model
from journal_sdk.utils.app_key import ApplicationKey as _ak


class Client:
    def __init__(self, http_client: HttpClient) -> None:
        self._client: AsyncClient = client
        self._transport: HttpClient = (
            transport if transport else HttpClient(self._client)
        )
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
            url=JournalEndpoints.AUTH_URL.value,
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
        raise exceptions.InvalidJWTError()

    async def get_schedule(
        self,
        token: str,
        strdate: str | date | None = None,
        raw: bool | None = False,
    ):
        if not strdate:  # Handle not provided date param
            strdate = date.today()

        if token:
            _sch_response: Response = await self._transport.request(
                method="get",
                url=JournalEndpoints.SCHEDULE_URL.value,
                token=token,
                params={"date": str(strdate)},
            )

            if raw:
                return _sch_response.json()

            # Parse raw schedule data to object
            _schedule_object: _sch_model = _sch_model(lessons=_sch_response.json())

            if _schedule_object:
                return _schedule_object

        raise exceptions.InvalidJWTError()

    async def get_homework(
        self, token: str, raw: bool = False
    ) -> dict[int, int] | _hw_model | Any:
        if token:
            _hw_response: Response = await self._transport.request(
                method="get",
                url=JournalEndpoints.STUDENT_HOMEWORK.value,
                token=token,
            )

            if raw:
                return _hw_response.json()

            _homework_object: _hw_model = _hw_model(counters=_hw_response.json())

            if _homework_object:
                return _homework_object

        raise exceptions.InvalidJWTError()

    async def get_avg_score(self, token: str, raw: bool = False):
        if token:
            _score_response: Response = await self._transport.request(
                method="get", url=JournalEndpoints.METRIC_GRADE.value, token=token
            )

            if raw:
                return _score_response.json()

        raise exceptions.InvalidJWTError()

    async def get_user_info(self, token: str, raw: bool | None = False):
        if token:
            _inf_response: Response = await self._transport.request(
                method="get", url=JournalEndpoints.USER_INFO.value, token=token
            )

            if raw:
                return _inf_response.json()

            _user_info_object: Any = _uf_model(**_inf_response.json())

            if _user_info_object:
                return _user_info_object
        raise exceptions.InvalidJWTError()

    async def close_connection(self) -> None:
        """Close async connection with private client object"""
        await self._client.aclose()

        return None
