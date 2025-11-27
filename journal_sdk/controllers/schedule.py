from datetime import date

from rapid_api_client import get

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.schedule import LessonResponse, ScheduleResponse
from journal_sdk.rapid.client import BaseController


class ScheduleController(BaseController):
    """
    Class schedule controller.

    Manages retrieval of class schedules and lesson information.
    Provides access to daily schedules, lesson details, and
    class timing information for students and instructors.

    Контроллер расписания занятий.

    Управляет получением расписания занятий и информации об уроках.
    Предоставляет доступ к ежедневным расписаниям, деталям уроков и
    информации о времени занятий для студентов и преподавателей.
    """

    @get(endpoints.SCHEDULE_BY_DATE.value)
    async def get_lesson_list_by_date(self, date: date) -> list[LessonResponse]:  # pyright: ignore[reportUnusedParameter]
        """
        Get list of lessons scheduled for a specific date.

        Retrieves all scheduled lessons for the provided date,
        including subject information, timing, instructor details,
        and classroom location for each lesson.

        Получить список уроков, запланированных на определенную дату.

        Возвращает все запланированные уроки на указанную дату,
        включая информацию о предметах, времени, детали преподавателя
        и местоположение аудитории для каждого урока.

        Args:
            date:
                The date for which to retrieve the lesson schedule.

                Дата, на которую нужно получить расписание уроков.

        Returns:
            list[LessonResponse]:
                List of lessons scheduled for the specified date with complete information.

                Список уроков, запланированных на указанную дату, с полной информацией.
        """
        ...

    async def get_schedule_by_date(self, date: date) -> ScheduleResponse:
        """
        Get complete schedule for a specific date in response wrapper.

        Combines individual lesson data into a comprehensive schedule object
        that provides organized access to all classes for the specified date
        with additional metadata and scheduling information.

        Получить полное расписание на определенную дату в обертке ответа.

        Комбинирует индивидуальные данные об уроках в комплексный объект расписания,
        который предоставляет организованный доступ ко всем классам на указанную дату
        с дополнительными метаданными и информацией о расписании.

        Args:
            date:
                The date for which to retrieve the complete schedule.

                Дата, на которую нужно получить полное расписание.

        Returns:
            ScheduleResponse:
                Complete schedule object with organized lesson data and metadata.

                Полный объект расписания с организованными данными об уроках и метаданными.
        """
        return ScheduleResponse(lesson_list=await self.get_lesson_list_by_date(date))
