from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import httpx
from httpx import AsyncClient, Response
from rapid_api_client import RapidApi

from top_journal_sdk.exceptions import RequestTimeoutError, translate_http_error


class BaseController(RapidApi):
    """
    Базовый контроллер SDK с единым переводом транспортных ошибок.

    Base controller with unified translation of transport errors.

    Все HTTP-статусные ошибки (httpx.HTTPStatusError) преобразуются в доменные
    исключения top_journal_sdk.exceptions, таймауты — в RequestTimeoutError,
    поэтому вызывающий код работает с одной иерархией исключений.
    """

    def process_response(
        self,
        response: Response,
        response_class: type[Any],
        raise_for_status: bool | None = None,
    ) -> Any:
        try:
            return super().process_response(
                response, response_class, raise_for_status=raise_for_status
            )
        except httpx.HTTPStatusError as exc:
            mapped = translate_http_error(exc)
            if mapped is None:
                raise
            raise mapped from exc

    @asynccontextmanager
    async def async_client(self) -> AsyncGenerator[AsyncClient, None]:
        try:
            async with super().async_client() as client:
                yield client
        except httpx.TimeoutException as exc:
            raise RequestTimeoutError() from exc
