from rapid_api_client import get

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.homework import (
    HomeworkCounterResponse,
    HomeworksResponse,
)
from journal_sdk.rapid.client import BaseController


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

    @get(endpoints.HOMEWORK_COUNT.value)
    async def get_homework_count_list(self) -> list[HomeworkCounterResponse]:
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

    async def get_homeworks(self) -> HomeworksResponse:
        """
        Get complete homework information for the student.

        Combines homework count data into a comprehensive object
        that provides an overview of all homework assignments and
        their completion status across different categories.

        Получить полную информацию о домашних заданиях студента.

        Комбинирует данные о количестве заданий в комплексный объект,
        который предоставляет обзор всех домашних заданий и
        их статуса выполнения по разным категориям.

        Returns:
            HomeworksResponse:
                Complete homework assignments object with categorized statistics.

                Полный объект домашних заданий с категоризированной статистикой.
        """
        return HomeworksResponse(counter_list=await self.get_homework_count_list())
