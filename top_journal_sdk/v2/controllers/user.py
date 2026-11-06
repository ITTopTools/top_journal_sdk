from __future__ import annotations

from top_journal_sdk.v2.controllers.base import BaseController
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints
from top_journal_sdk.v2.models.user import UserInfoResponse


class UserController(BaseController):
    """Контроллер пользователя для journalka API v2."""

    async def get_personal_info(self) -> UserInfoResponse:
        """
        Получить информацию о текущем пользователе.

        GET /api/dashboard/user-info
        """
        response = await self.sdk.get(endpoints.DASHBOARD_USER_INFO.value)
        response.raise_for_status()
        return UserInfoResponse.model_validate(response.json())
