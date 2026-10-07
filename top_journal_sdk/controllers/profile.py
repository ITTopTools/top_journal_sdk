from typing import Annotated

from httpx import Response
from rapid_api_client import PydanticBody, Query, get, post

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.profile import (
    ChangeCurrentGroupRequest,
    ProfileFormsResponse,
    ProfileFormResponse,
    ProfileSettingsResponse,
    StudentAchievementsResponse,
    StudentAchievementResponse,
)
from top_journal_sdk.models.spec import SpecsResponse, SpecModel
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class ProfileController(BaseController):
    """
    Profile controller.

    Handles retrieval of profile settings, achievements, specs and documents.

    Контроллер профиля.

    Обрабатывает получение настроек профиля, достижений, предметов и документов.
    """

    @with_auth_refresh
    @get(endpoints.PROFILE_SETTINGS.value)
    async def get_profile_settings(self) -> ProfileSettingsResponse:
        """
        Get student profile settings.

        Получить настройки профиля студента.

        Returns:
            ProfileSettingsResponse: Profile settings / Настройки профиля.
        """
        ...

    @with_auth_refresh
    @get(endpoints.PROFILE_ACHIEVEMENTS.value)
    async def get_student_achievement_list(
        self,
    ) -> list[StudentAchievementResponse]:
        """
        Get student achievements.

        Получить достижения студента.

        Returns:
            list[StudentAchievementResponse]: Achievements / Достижения.
        """
        ...

    async def get_student_achievements(self) -> StudentAchievementsResponse:
        """
        Get student achievements in response wrapper.

        Получить достижения студента в обертке ответа.

        Returns:
            StudentAchievementsResponse: Achievements object / Объект достижений.
        """
        return StudentAchievementsResponse(
            student_achievement_list=await self.get_student_achievement_list()
        )

    @with_auth_refresh
    @get(endpoints.DOCUMENTS_PROFILE_FIELDS.value)
    async def get_profile_field_list(
        self,
        student_id: Annotated[int, Query(alias="studentId")],  # pyright: ignore[reportUnusedParameter]
    ) -> list[ProfileFormResponse]:
        """
        Get profile fields for documents.

        Получить поля профиля для документов.

        Args:
            student_id: Student ID (sent as `studentId`) / ID студента.

        Returns:
            list[ProfileFormResponse]: Profile fields / Поля профиля.
        """
        ...

    async def get_profile_fields(
        self, student_id: int | None = None
    ) -> ProfileFormsResponse:
        """
        Get profile fields for documents in response wrapper.

        Получить поля профиля для документов в обертке ответа.

        Args:
            student_id: Student ID (defaults to session) / ID студента.

        Returns:
            ProfileFormsResponse: Fields object / Объект полей.
        """
        resolved_student_id = self.resolve_student_id(student_id)
        return ProfileFormsResponse(
            profile_form_list=await self.get_profile_field_list(resolved_student_id)
        )

    @with_auth_refresh
    @get(endpoints.SETTINGS_GROUP_SPECS.value)
    async def get_group_spec_list(
        self,
        include_planned: Annotated[bool, Query()] = False,  # pyright: ignore[reportUnusedParameter]
    ) -> list[SpecModel]:
        """
        Get current group specs.

        Получить предметы текущей группы.

        Args:
            include_planned: Include planned specs / Включая планируемые.

        Returns:
            list[SpecModel]: Group specs / Предметы группы.
        """
        ...

    async def get_group_specs(
        self, include_planned: bool = False
    ) -> SpecsResponse:
        """
        Get current group specs in response wrapper.

        Получить предметы текущей группы в обертке ответа.

        Args:
            include_planned: Include planned specs / Включая планируемые.

        Returns:
            SpecsResponse: Specs object / Объект предметов.
        """
        return SpecsResponse(
            spec_list=await self.get_group_spec_list(include_planned)
        )

    @with_auth_refresh
    @get(endpoints.SETTINGS_HISTORY_SPECS.value)
    async def get_history_spec_list(
        self,
        include_planned: Annotated[bool, Query()] = False,  # pyright: ignore[reportUnusedParameter]
    ) -> list[SpecModel]:
        """
        Get history specs.

        Получить историю предметов.

        Args:
            include_planned: Include planned specs / Включая планируемые.

        Returns:
            list[SpecModel]: History specs / История предметов.
        """
        ...

    async def get_history_specs(
        self, include_planned: bool = False
    ) -> SpecsResponse:
        """
        Get history specs in response wrapper.

        Получить историю предметов в обертке ответа.

        Args:
            include_planned: Include planned specs / Включая планируемые.

        Returns:
            SpecsResponse: Specs object / Объект предметов.
        """
        return SpecsResponse(
            spec_list=await self.get_history_spec_list(include_planned)
        )

    @with_auth_refresh
    @get(endpoints.SETTINGS_PUBLIC_FORMS.value)
    async def get_public_form_list(self) -> list[ProfileFormResponse]:
        """
        Get public settings forms.

        Получить публичные формы настроек.

        Returns:
            list[ProfileFormResponse]: Public forms / Публичные формы.
        """
        ...

    async def get_public_forms(self) -> ProfileFormsResponse:
        """
        Get public settings forms in response wrapper.

        Получить публичные формы настроек в обертке ответа.

        Returns:
            ProfileFormsResponse: Forms object / Объект форм.
        """
        return ProfileFormsResponse(
            profile_form_list=await self.get_public_form_list()
        )

    @with_auth_refresh
    @post(endpoints.SETTINGS_CHANGE_GROUP.value, raise_for_status=True)
    async def post_change_current_group_response(
        self,
        body: Annotated[ChangeCurrentGroupRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> Response:
        """
        Change current group (raw response).

        Сменить текущую группу (сырой ответ).
        """
        ...

    async def post_change_current_group(self, group_id: int) -> bool:
        """
        Change current group.

        Сменить текущую группу. При успехе контекст сессии обновляется.

        Args:
            group_id: New current group ID / ID новой текущей группы.

        Returns:
            True on success (raises on HTTP errors) / True при успехе.
        """
        response = await self.post_change_current_group_response(
            ChangeCurrentGroupRequest(id_tgroups=group_id)
        )
        if response.is_success and self.session is not None:
            self.session.group_id = group_id
        return response.is_success
