from __future__ import annotations

from top_journal_sdk.v2.controllers.base import BaseController
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints
from top_journal_sdk.v2.models.profile import (
    ChangeGroupResponse,
    DocumentFieldsResponse,
    DocumentsResponse,
    ProfileSettingsResponse,
)


class ProfileController(BaseController):
    """Контроллер профиля для journalka API v2."""

    async def get_settings(self) -> ProfileSettingsResponse:
        """GET /api/dashboard/profile/settings"""
        response = await self.sdk.get(endpoints.PROFILE_SETTINGS.value)
        response.raise_for_status()
        return ProfileSettingsResponse.model_validate(response.json())

    async def get_documents(self, student_id: int | None = None) -> DocumentsResponse:
        """GET /api/dashboard/profile/documents?studentId=..."""
        params: dict[str, object] = {}
        if student_id is not None:
            params["studentId"] = student_id
        response = await self.sdk.get(endpoints.PROFILE_DOCUMENTS.value, params=params)
        response.raise_for_status()
        return DocumentsResponse.model_validate(response.json())

    async def get_documents_fields(self, student_id: int | None = None) -> DocumentFieldsResponse:
        """GET /api/dashboard/profile/documents/fields?studentId=..."""
        params: dict[str, object] = {}
        if student_id is not None:
            params["studentId"] = student_id
        response = await self.sdk.get(endpoints.PROFILE_DOCUMENTS_FIELDS.value, params=params)
        response.raise_for_status()
        return DocumentFieldsResponse.model_validate(response.json())

    async def change_group(self, group_id: int | str) -> ChangeGroupResponse:
        """POST /api/dashboard/groups/change"""
        response = await self.sdk.post(
            endpoints.GROUPS_CHANGE.value,
            json={"groupId": group_id},
        )
        response.raise_for_status()
        if not response.content:
            return ChangeGroupResponse()
        return ChangeGroupResponse.model_validate(response.json())
