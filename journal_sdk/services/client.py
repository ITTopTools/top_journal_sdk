from datetime import date
from typing import Any, cast

from httpx import Response

from journal_sdk.enums.endpoints import JournalEndpoints
from journal_sdk.http.client import HttpClient
from journal_sdk.models.homework import Homeworks as _hw_model
from journal_sdk.models.schedule import Schedule as _sch_model
from journal_sdk.models.user_info import UserInfo as _uf_model
from journal_sdk.utils.app_key import ApplicationKey


class Client:
    def __init__(self, http_client: HttpClient) -> None:
        self.client: HttpClient = http_client
        self._app_key: ApplicationKey = ApplicationKey()

    async def login(self, username: str, password: str, raw: bool | None = False) -> str:
        auth_data = {
            "application_key": await self._app_key.get_key(True),
            "username": username,
            "password": password,
            "id_city": None,
        }
        response: Response = await self.client.post(
            url=JournalEndpoints.AUTH_URL.value,
            params=None,
            json=auth_data,
        )
        if raw:
            return response.json()
        else:
            jwt_token: str = str(cast(dict[str, str], response.json()).get("access_token", ""))
            if jwt_token:
                return jwt_token

    async def get_schedule(
        self,
        token: str,
        strdate: str | date | None = None,
        raw: bool | None = False,
    ):
        if strdate is None:  # Handle not provided date param
            strdate = date.today()

        response: Response = await self.client.get(
            url=JournalEndpoints.SCHEDULE_URL.value,
            token=token,
            params={"date": str(strdate)},
        )

        if raw:
            return response.json()
        else:
            # Parse raw schedule data to object
            _schedule_object: _sch_model = _sch_model(lessons=response.json())
            if _schedule_object:
                return _schedule_object

    async def get_homework(
        self, token: str, raw: bool = False
    ) -> dict[int, int] | _hw_model | Any:
        response: Response = await self.client.get(
            url=JournalEndpoints.STUDENT_HOMEWORK.value,
            token=token,
        )
        if raw:
            return response.json()
        else:
            _homework_object: _hw_model = _hw_model(counters=response.json())
            if _homework_object:
                return _homework_object

    async def get_avg_score(self, token: str, raw: bool = False):
        response: Response = await self.client.get(
            url=JournalEndpoints.METRIC_GRADE.value, token=token
        )
        if raw:
            return response.json()

    async def get_user_info(self, token: str, raw: bool | None = False):
        response: Response = await self.client.get(
            url=JournalEndpoints.USER_INFO.value, token=token
        )
        if raw:
            return response.json()
        else:
            _user_info_object: Any = _uf_model(**response.json())
            if _user_info_object:
                return _user_info_object
