from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Concatenate, ParamSpec, TypeVar

import httpx
from httpx import AsyncClient, Response
from rapid_api_client import RapidApi

from top_journal_sdk.exceptions import (
    OutdatedJWTError,
    RequestTimeoutError,
    translate_http_error,
)
from top_journal_sdk.session import SessionContext

P = ParamSpec("P")
R = TypeVar("R")


class BaseController(RapidApi):
    """
    Базовый контроллер SDK с единым переводом транспортных ошибок.

    Base controller with unified translation of transport errors.

    Все HTTP-статусные ошибки (httpx.HTTPStatusError) преобразуются в доменные
    исключения top_journal_sdk.exceptions, таймауты — в RequestTimeoutError,
    поэтому вызывающий код работает с одной иерархией исключений.
    """

    def __init__(
        self,
        *args: Any,
        session: SessionContext | None = None,
        refresh_handler: Callable[[], Awaitable[None]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.session = session
        self.refresh_handler = refresh_handler

    def resolve_group_id(self, group_id: int | None) -> int:
        """
        Возвращает group_id: явный или из контекста сессии после login().

        Returns group_id: explicit or from the post-login session context.
        """
        if group_id is not None:
            return group_id
        if self.session is not None and self.session.group_id is not None:
            return self.session.group_id
        raise RuntimeError(
            "No group context. Login first or pass group_id explicitly."
        )

    def resolve_student_id(self, student_id: int | None) -> int:
        """
        Возвращает student_id: явный или из контекста сессии после login().

        Returns student_id: explicit or from the post-login session context.
        """
        if student_id is not None:
            return student_id
        if self.session is not None and self.session.student_id is not None:
            return self.session.student_id
        raise RuntimeError(
            "No student context. Login first or pass student_id explicitly."
        )

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


S = TypeVar("S", bound=BaseController)


def with_auth_refresh(
    func: Callable[Concatenate[S, P], Awaitable[R]],
) -> Callable[Concatenate[S, P], Awaitable[R]]:
    """
    Декоратор: при протухшем JWT один раз обновляет токены и повторяет вызов.

    Decorator: on an outdated JWT, refreshes tokens once and retries the call.

    Хендлер обновления выставляет SDK (см. TopJournalSDK._refresh_access_token).
    Без хендлера исходное исключение пробрасывается как есть.
    """

    @wraps(func)
    async def wrapper(self: S, *args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(self, *args, **kwargs)
        except OutdatedJWTError:
            if self.refresh_handler is None:
                raise
            await self.refresh_handler()
            return await func(self, *args, **kwargs)

    return wrapper
