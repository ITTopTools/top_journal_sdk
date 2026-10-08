import httpx
import pytest

import top_journal_sdk.exceptions as errors
from top_journal_sdk.controllers import UserInfoController
from top_journal_sdk.models.user import UserResponse


def _response(status: int) -> httpx.Response:
    request = httpx.Request("GET", "https://msapi.top-academy.ru/api/v2/x")
    return httpx.Response(status, request=request)


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (401, errors.OutdatedJWTError),
        (403, errors.InvalidJWTError),
        (404, errors.DataNotFoundError),
        (408, errors.RequestTimeoutError),
        (410, errors.InvalidAppKeyError),
        (422, errors.InvalidAuthDataError),
        (500, errors.InternalServerError),
        (503, errors.InternalServerError),
    ],
)
def test_status_mapping(status: int, expected: type[errors.JournalException]) -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(expected):
        controller.process_response(_response(status), UserResponse)


def test_unmapped_status_reraises_original() -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(httpx.HTTPStatusError):
        controller.process_response(_response(418), UserResponse)


def test_mapped_errors_are_domain_errors() -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    with pytest.raises(errors.JournalException):
        controller.process_response(_response(401), UserResponse)


async def test_async_client_timeout_translation() -> None:
    controller = UserInfoController(async_client=httpx.AsyncClient())
    timeout_error = httpx.ConnectTimeout("boom")
    with pytest.raises(errors.RequestTimeoutError):
        async with controller.async_client():
            raise timeout_error
