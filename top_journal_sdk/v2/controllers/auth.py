from __future__ import annotations

from top_journal_sdk.v2.controllers.base import BaseController
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints
from top_journal_sdk.v2.models.auth import LoginRequest, LoginResponse, RefreshResponse


class AuthController(BaseController):
    """Контроллер авторизации для journalka API v2."""

    async def login(self, username: str, password: str) -> LoginResponse:
        """POST /api/auth/login — возвращает токены и устанавливает cookies."""
        response = await self.sdk.post(
            endpoints.AUTH_LOGIN.value,
            json=LoginRequest(username=username, password=password).model_dump(),
            refresh_on_401=False,
        )
        response.raise_for_status()
        # AsyncClient persists Set-Cookie with its original domain/path/expiry.
        return LoginResponse.model_validate(response.json())

    async def logout(self) -> bool:
        """POST /api/auth/logout"""
        response = await self.sdk.post(
            endpoints.AUTH_LOGOUT.value,
            refresh_on_401=False,
        )
        if response.is_success:
            for cookie in list(self.sdk.client.cookies.jar):
                if cookie.name.startswith("journal_"):
                    self.sdk.client.cookies.delete(
                        cookie.name, domain=cookie.domain, path=cookie.path
                    )
        return response.is_success

    async def refresh(self) -> RefreshResponse:
        """POST /api/auth/refresh"""
        response = await self.sdk.post(
            endpoints.AUTH_REFRESH.value,
            refresh_on_401=False,
        )
        response.raise_for_status()
        return RefreshResponse.model_validate(response.json())
