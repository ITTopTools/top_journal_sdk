from typing import Annotated

from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.homework import (
    GroupHistoriesResponse,
    GroupHistoryResponse,
    HomeworkCounterResponse,
    HomeworkListItemResponse,
    HomeworksListResponse,
    HomeworksResponse,
    HomeworkTagResponse,
    HomeworkTagsResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class HomeworkController(BaseController):
    """
    Student homework controller.

    Handles management and retrieval of homework assignments data.
    Provides statistics about homework completion status,
    overdue assignments, and overall homework progress.

    Контроллер домашних заданий студентов.

    Обрабатывает управление и получение данных о домашних заданиях.
    Предоставляет статистику о статусе выполнения домашних заданий,
    просроченных заданиях и общем прогрессе по домашним работам.
    """

    @with_auth_refresh
    @get(endpoints.HOMEWORK_COUNT.value)
    async def get_homework_count_list(
        self,
        group_id: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
        homework_type: Annotated[int | None, Query(alias="type")] = None,  # pyright: ignore[reportUnusedParameter]
    ) -> list[HomeworkCounterResponse]:
        """
        Get statistics about homework assignments by categories.

        Retrieves count information for different categories of homework:
        total assignments, overdue assignments, checked assignments,
        pending assignments, and current assignments.

        Получить статистику по домашним заданиям по категориям.

        Возвращает информацию о количестве в разных категориях домашних заданий:
        всего заданий, просроченных заданий, проверенных заданий,
        ожидающих проверки заданий и текущих заданий.

        Returns:
            list[HomeworkCounterResponse]:
                List of homework counters by different completion status categories.

                Список счетчиков домашних заданий по разным категориям статуса выполнения.
        """
        ...

    async def get_homeworks(
        self, group_id: int | None = None, homework_type: int | None = None
    ) -> HomeworksResponse:
        """
        Get complete homework information for the student.

        Combines homework count data into a comprehensive object
        that provides an overview of all homework assignments and
        their completion status across different categories.

        Получить полную информацию о домашних заданиях студента.

        Комбинирует данные о количестве заданий в комплексный объект,
        который предоставляет обзор всех домашних заданий и
        их статуса выполнения по разным категориям.

        Args:
            group_id: ID группы. По умолчанию из сессии после login().
                Group ID. Defaults to the post-login session value.
            homework_type: Тип домашних заданий (как шлет фронт в `type`).
                Homework type (as the frontend sends it in `type`).

        Returns:
            HomeworksResponse:
                Complete homework assignments object with categorized statistics.

                Полный объект домашних заданий с категоризированной статистикой.
        """
        resolved_group_id = self.resolve_group_id(group_id)
        return HomeworksResponse(
            counter_list=await self.get_homework_count_list(
                resolved_group_id, homework_type
            )
        )

    @with_auth_refresh
    @get(endpoints.HOMEWORK_LIST.value)
    async def get_homework_list(
        self,
        group_id: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
        page: Annotated[int, Query()] = 1,  # pyright: ignore[reportUnusedParameter]
        status: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
        homework_type: Annotated[int | None, Query(alias="type")] = None,  # pyright: ignore[reportUnusedParameter]
    ) -> list[HomeworkListItemResponse]:
        """
        Get paginated homework assignment list.

        Получить постраничный список домашних заданий.

        Args:
            group_id: Group ID (defaults to session) / ID группы (по умолчанию из сессии).
            page: Page number, 1-based / Номер страницы с 1.
            status: Homework status filter / Фильтр по статусу.
            homework_type: Homework type filter (sent as `type`) / Фильтр по типу.

        Returns:
            list[HomeworkListItemResponse]: Homework entries / Записи домашних заданий.
        """
        ...

    async def get_homeworks_list(
        self,
        group_id: int | None = None,
        page: int = 1,
        status: int | None = None,
        homework_type: int | None = None,
    ) -> HomeworksListResponse:
        """
        Get homework assignment list in response wrapper.

        Получить список домашних заданий в обертке ответа.

        Args:
            group_id: Group ID (defaults to session) / ID группы (по умолчанию из сессии).
            page: Page number, 1-based / Номер страницы с 1.
            status: Homework status filter / Фильтр по статусу.
            homework_type: Homework type filter / Фильтр по типу.

        Returns:
            HomeworksListResponse: Homework list object / Объект списка домашних заданий.
        """
        resolved_group_id = self.resolve_group_id(group_id)
        return HomeworksListResponse(
            homework_list=await self.get_homework_list(
                resolved_group_id, page, status, homework_type
            )
        )

    @with_auth_refresh
    @get(endpoints.HOMEWORK_EVALUATION_TAGS.value)
    async def get_homework_tag_list(self) -> list[HomeworkTagResponse]:
        """
        Get homework evaluation tags.

        Получить теги оценки домашних заданий.

        Returns:
            list[HomeworkTagResponse]: Evaluation tags / Теги оценки.
        """
        ...

    async def get_homework_tags(self) -> HomeworkTagsResponse:
        """
        Get homework evaluation tags in response wrapper.

        Получить теги оценки домашних заданий в обертке ответа.

        Returns:
            HomeworkTagsResponse: Tags object / Объект тегов.
        """
        return HomeworkTagsResponse(
            homework_tag_list=await self.get_homework_tag_list()
        )

    @with_auth_refresh
    @get(endpoints.HOMEWORK_GROUP_HISTORY.value)
    async def get_group_history_list(self) -> list[GroupHistoryResponse]:
        """
        Get homework group history.

        Получить историю групп по домашним заданиям.

        Returns:
            list[GroupHistoryResponse]: Group history entries / Записи истории групп.
        """
        ...

    async def get_group_histories(self) -> GroupHistoriesResponse:
        """
        Get homework group history in response wrapper.

        Получить историю групп по домашним заданиям в обертке ответа.

        Returns:
            GroupHistoriesResponse: History object / Объект истории.
        """
        return GroupHistoriesResponse(
            group_history_list=await self.get_group_history_list()
        )
