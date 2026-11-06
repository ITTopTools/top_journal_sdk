from __future__ import annotations

import logging
from asyncio import Lock
from types import TracebackType
from typing import Any

import httpx

from top_journal_sdk.v2.controllers.auth import AuthController
from top_journal_sdk.v2.controllers.dashboard import DashboardController
from top_journal_sdk.v2.controllers.profile import ProfileController
from top_journal_sdk.v2.controllers.user import UserController
from top_journal_sdk.v2.ddg import DdgCookieManager
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints
from top_journal_sdk.v2.models.auth import LoginResponse, RefreshResponse

logger = logging.getLogger(__name__)

_CLIENT_NOT_INITIALIZED = "SDK not initialized. Call initialize() first."


class TopJournalSDKV2:
    """
    SDK v2 для journalka.top-academy.ru.

    Использует cookie-авторизацию (токены в HttpOnly cookies, не Bearer).
    Поддерживает автоматическое обновление сессии и получение __ddg* кук
    DDoS-Guard через Playwright при получении 401 на защищённые эндпоинты.
    """

    def __init__(
        self,
        timeout: float = 30.0,
        user_agent: str | None = None,
        ddg_cookies: dict[str, str] | None = None,
        *,
        auto_refresh_ddg: bool = True,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._timeout = timeout
        self._user_agent = user_agent or (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        )
        self._extra_headers = dict(extra_headers) if extra_headers is not None else {}

        self._client: httpx.AsyncClient | None = None
        self._ddg = DdgCookieManager(auto_refresh=auto_refresh_ddg)
        self._refresh_lock = Lock()
        self._session_generation = 0

        if ddg_cookies is not None:
            self._ddg.set_ddg_cookies(ddg_cookies)

        self._auth_controller: AuthController | None = None
        self._user_controller: UserController | None = None
        self._dashboard_controller: DashboardController | None = None
        self._profile_controller: ProfileController | None = None

    async def __aenter__(self) -> TopJournalSDKV2:
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def initialize(self) -> None:
        if self._client is not None:
            return
        client = httpx.AsyncClient(
            base_url=endpoints.JOURNALKA_BASE_URL.value,
            follow_redirects=True,
            timeout=self._timeout,
        )
        headers: dict[str, str] = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": endpoints.JOURNALKA_BASE_URL.value,
            "Referer": endpoints.JOURNALKA_BASE_URL.value + "/",
            "User-Agent": self._user_agent,
        }
        headers.update(self._extra_headers)
        client.headers.update(headers)
        self._client = client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
        self._auth_controller = None
        self._user_controller = None
        self._dashboard_controller = None
        self._profile_controller = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError(_CLIENT_NOT_INITIALIZED)
        return self._client

    @property
    def ddg(self) -> DdgCookieManager:
        return self._ddg

    def set_ddg_cookies(self, cookies: dict[str, str]) -> None:
        """Установить __ddg* куки вручную."""
        self._ddg.set_ddg_cookies(cookies)

    def _sync_ddg_cookies(self) -> None:
        """Подмешать текущие __ddg* куки в httpx клиент."""
        if self._client is None:
            return
        for name, value in self._ddg.cookies.items():
            self._client.cookies.set(name, value, domain="journalka.top-academy.ru", path="/")

    def _has_refresh_cookie(self) -> bool:
        return self._client is not None and any(
            cookie.name == "journal_refresh_token" for cookie in self._client.cookies.jar
        )

    async def _try_refresh_session(self) -> bool:
        """Обновить auth-сессию по refresh-cookie. Возвращает True при успехе."""
        try:
            result = await self.refresh()
        except httpx.HTTPError:
            logger.debug("v2 auth refresh after 401 failed", exc_info=True)
            return False
        else:
            return result.ok

    async def _request(
        self,
        method: str,
        path: str,
        *,
        refresh_on_401: bool = True,
        **kwargs: Any,
    ) -> httpx.Response:
        if self._client is None:
            await self.initialize()
        self._sync_ddg_cookies()
        generation = self._session_generation
        response = await self.client.request(method, path, **kwargs)

        if response.status_code != 401 or not refresh_on_401:
            return response

        # 1. Пробуем обновить auth-сессию по refresh-cookie (дёшево).
        async with self._refresh_lock:
            refreshed = generation != self._session_generation
            if not refreshed and self._has_refresh_cookie():
                refreshed = await self._try_refresh_session()
                if refreshed:
                    self._session_generation += 1
        if refreshed:
            response = await self.client.request(method, path, **kwargs)
            if response.status_code != 401:
                return response

        # 2. Затем пробуем обновить __ddg* куки через браузер.
        if self._ddg.should_auto_refresh():
            try:
                await self._ddg.refresh_via_playwright()
            except RuntimeError:
                logger.warning("Не удалось обновить __ddg* куки", exc_info=True)
            else:
                self._sync_ddg_cookies()
                response = await self.client.request(method, path, **kwargs)

        return response

    async def get(
        self, path: str, *, refresh_on_401: bool = True, **kwargs: Any
    ) -> httpx.Response:
        return await self._request("GET", path, refresh_on_401=refresh_on_401, **kwargs)

    async def post(
        self, path: str, *, refresh_on_401: bool = True, **kwargs: Any
    ) -> httpx.Response:
        return await self._request("POST", path, refresh_on_401=refresh_on_401, **kwargs)

    # ----- Auth -----

    async def login(self, username: str, password: str) -> LoginResponse:
        """
        Авторизоваться в journalka API v2.
        Токены приходят в Set-Cookie (journal_access_token, journal_refresh_token и т.д.).
        """
        return await self.auth.login(username, password)

    async def logout(self) -> bool:
        """Выйти из сессии."""
        return await self.auth.logout()

    async def refresh(self) -> RefreshResponse:
        """Обновить сессию через refresh cookie (из cookies клиента)."""
        return await self.auth.refresh()

    # ----- Controllers -----

    @property
    def auth(self) -> AuthController:
        if self._auth_controller is None:
            self._auth_controller = AuthController(self)
        return self._auth_controller

    @property
    def user(self) -> UserController:
        if self._user_controller is None:
            self._user_controller = UserController(self)
        return self._user_controller

    @property
    def dashboard(self) -> DashboardController:
        if self._dashboard_controller is None:
            self._dashboard_controller = DashboardController(self)
        return self._dashboard_controller

    @property
    def profile(self) -> ProfileController:
        if self._profile_controller is None:
            self._profile_controller = ProfileController(self)
        return self._profile_controller
