from rapid_api_client import get

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.attendance import (
    AttendanceResponse,
    AttendancesResponse,
)
from journal_sdk.rapid.client import BaseController


class AttendanceController(BaseController):
    """
    Student attendance controller.

    Manages retrieval of attendance data for students.
    Provides information about class attendance patterns,
    absences, and overall attendance statistics.

    Контроллер посещаемости студентов.

    Управляет получением данных о посещаемости студентов.
    Предоставляет информацию о посещаемости занятий,
    пропусках и общей статистике посещаемости.
    """

    @get(endpoints.ATTENDANCE_DATA.value)
    async def get_attendance_list(self) -> list[AttendanceResponse]:
        """
        Get detailed list of student attendance records.

        Retrieves comprehensive data about student attendance
        including presence/absence records and attendance patterns
        for different classes and time periods.

        Получить подробный список записей о посещаемости студента.

        Возвращает комплексные данные о посещаемости студента,
        включая записи о присутствии/отсутствии и паттерны посещаемости
        для разных классов и временных периодов.

        Returns:
            list[AttendanceResponse]:
                List of detailed attendance records with comprehensive information.

                Список подробных записей о посещаемости с комплексной информацией.
        """
        ...

    async def get_attendances(self) -> AttendancesResponse:
        """
        Get attendance data in a comprehensive response wrapper.

        Combines individual attendance records into a complete response object
        that provides an overview of the student's attendance statistics
        and overall attendance performance.

        Получить данные о посещаемости в комплексной обертке ответа.

        Комбинирует индивидуальные записи о посещаемости в полный объект ответа,
        который предоставляет обзор статистики посещаемости студента
        и общей успеваемости посещаемости.

        Returns:
            AttendancesResponse:
                Object with comprehensive attendance statistics and summary.

                Объект с комплексной статистикой посещаемости и сводкой.
        """
        return AttendancesResponse(attendance_list=await self.get_attendance_list())
