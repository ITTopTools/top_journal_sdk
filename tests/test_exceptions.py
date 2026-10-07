import httpx
import pytest

import top_journal_sdk.exceptions as E
from top_journal_sdk.controllers import UserInfoController
from top_journal_sdk.models.user import UserResponse


def _response(status: int) -> httpx.Response:
    request = httpx.Request("GET", "https://msapi.top-academy.ru/api/v2/x")
    return httpx.Response(status, request=request)


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (401, E.OutdatedJWTError),
        (403, E.InvalidJWTError),
        (404, E.DataNotFoundError),
        (408, E.RequestTimeoutError),
        (410, E.InvalidAppKeyError),
        (422, E.InvalidAuthDataError),
        (500, E.InternalServerError),
        (503, E.InternalServerError),
    ],
)
def test_status_mapping(status: int, expected: type[E.JournalException]) -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(expected):
        controller.process_response(_response(status), UserResponse)


def test_unmapped_status_reraises_original() -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(httpx.HTTPStatusError):
        controller.process_response(_response(418), UserResponse)


def test_mapped_errors_are_domain_errors() -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(E.JournalException):
        controller.process_response(_response(401), UserResponse)


async def test_async_client_timeout_translation() -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(E.RequestTimeoutError):
        async with controller.async_client():
            raise httpx.ConnectTimeout("boom")
