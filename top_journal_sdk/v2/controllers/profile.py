from __future__ import annotations

from typing import Any, cast

from top_journal_sdk.v2.controllers.base import BaseController
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints
from top_journal_sdk.v2.models.profile import (
    DocumentsResponse,
    ProfileSettingsResponse,
)


class ProfileController(BaseController):
    """Контроллер профиля для journalka API v2."""

    async def get_settings(self) -> ProfileSettingsResponse:
        """GET /api/dashboard/profile/settings"""
        response = await self.sdk.get(endpoints.PROFILE_SETTINGS.value)
        response.raise_for_status()
        return ProfileSettingsResponse(**response.json())

    async def get_documents(self, student_id: int | None = None) -> DocumentsResponse:
        """GET /api/dashboard/profile/documents?studentId=..."""
        params: dict[str, object] = {}
        if student_id is not None:
            params["studentId"] = student_id
        response = await self.sdk.get(endpoints.PROFILE_DOCUMENTS.value, params=params)
        response.raise_for_status()
        return DocumentsResponse(**response.json())

    async def get_documents_fields(self, student_id: int | None = None) -> dict[str, Any]:
        """GET /api/dashboard/profile/documents/fields?studentId=..."""
        params: dict[str, object] = {}
        if student_id is not None:
            params["studentId"] = student_id
        response = await self.sdk.get(endpoints.PROFILE_DOCUMENTS_FIELDS.value, params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    async def change_group(self, group_id: int | str) -> dict[str, Any]:
        """POST /api/dashboard/groups/change"""
        response = await self.sdk.post(
            endpoints.GROUPS_CHANGE.value,
            json={"groupId": group_id},
        )
        response.raise_for_status()
        return cast(dict[str, Any], response.json())
