from typing import Annotated

from httpx import Response
from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.library import (
    LibraryCountResponse,
    LibraryCountsResponse,
    LibraryMaterialResponse,
    LibraryMaterialsResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class LibraryController(BaseController):
    """
    Library controller.

    Handles retrieval of library materials, counters and quizzes.

    Контроллер библиотеки.

    Обрабатывает получение материалов библиотеки, счетчиков и опросов.
    """

    @with_auth_refresh
    @get(endpoints.LIBRARY_LIST.value)
    async def get_library_material_list(
        self,
        material_type: Annotated[int, Query()],  # pyright: ignore[reportUnusedParameter]
        recommended_type: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
        spec_id: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
    ) -> list[LibraryMaterialResponse]:
        """
        Get library materials list.

        Получить список материалов библиотеки.

        Args:
            material_type: Material type / Тип материала.
            recommended_type: Recommended type filter / Фильтр рекомендаций.
            spec_id: Subject filter / Фильтр по предмету.

        Returns:
            list[LibraryMaterialResponse]: Materials / Материалы.
        """
        ...

    async def get_library_materials(
        self,
        material_type: int,
        recommended_type: int | None = None,
        spec_id: int | None = None,
    ) -> LibraryMaterialsResponse:
        """
        Get library materials in response wrapper.

        Получить материалы библиотеки в обертке ответа.

        Args:
            material_type: Material type / Тип материала.
            recommended_type: Recommended type filter / Фильтр рекомендаций.
            spec_id: Subject filter / Фильтр по предмету.

        Returns:
            LibraryMaterialsResponse: Materials object / Объект материалов.
        """
        return LibraryMaterialsResponse(
            library_material_list=await self.get_library_material_list(
                material_type, recommended_type, spec_id
            )
        )

    @with_auth_refresh
    @get(endpoints.LIBRARY_COUNT.value)
    async def get_library_count_list(
        self,
        material_type: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
        recommended_type: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
    ) -> list[LibraryCountResponse]:
        """
        Get library counters.

        Получить счетчики библиотеки.

        Args:
            material_type: Material type / Тип материала.
            recommended_type: Recommended type filter / Фильтр рекомендаций.

        Returns:
            list[LibraryCountResponse]: Counters / Счетчики.
        """
        ...

    async def get_library_counts(
        self,
        material_type: int | None = None,
        recommended_type: int | None = None,
    ) -> LibraryCountsResponse:
        """
        Get library counters in response wrapper.

        Получить счетчики библиотеки в обертке ответа.

        Args:
            material_type: Material type / Тип материала.
            recommended_type: Recommended type filter / Фильтр рекомендаций.

        Returns:
            LibraryCountsResponse: Counters object / Объект счетчиков.
        """
        return LibraryCountsResponse(
            library_count_list=await self.get_library_count_list(material_type, recommended_type)
        )

    @with_auth_refresh
    @get(endpoints.LIBRARY_QUIZ_INTERVIEW.value, raise_for_status=True)
    async def get_quiz_interview_response(self) -> Response:
        """
        Get library opened interview state (raw response, 204 when empty).

        Получить состояние открытого интервью (сырой ответ, 204 если пусто).
        """
        ...

    async def has_opened_interview(self) -> bool:
        """
        Check whether a library interview is opened.

        Проверить, открыто ли интервью библиотеки.

        Returns:
            True when interview data exists / True если данные есть.
        """
        response: Response = await self.get_quiz_interview_response()
        return response.status_code == 200
