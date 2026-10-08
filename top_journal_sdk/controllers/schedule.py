from datetime import date
from typing import Annotated

from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.schedule import (
    LessonResponse,
    MonthEventResponse,
    MonthEventsResponse,
    ScheduleResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


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

    @with_auth_refresh
    @get(endpoints.SCHEDULE_BY_DATE.value)
    async def get_lesson_list_by_date(
        self,
        date_filter: Annotated[date, Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> list[LessonResponse]:
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

    async def get_schedule_by_date(self, target_date: date) -> ScheduleResponse:
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
            target_date:
                The date for which to retrieve the complete schedule.

                Дата, на которую нужно получить полное расписание.

        Returns:
            ScheduleResponse:
                Complete schedule object with organized lesson data and metadata.

                Полный объект расписания с организованными данными об уроках и метаданными.
        """
        return ScheduleResponse(lesson_list=await self.get_lesson_list_by_date(target_date))

    @with_auth_refresh
    @get(endpoints.SCHEDULE_BY_MONTH.value)
    async def get_month_lesson_list(
        self,
        date_filter: Annotated[date, Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> list[LessonResponse]:
        """
        Get list of lessons scheduled for a calendar month.

        Month is selected by any date inside it (frontend sends date_filter).

        Получить список уроков за календарный месяц.

        Месяц выбирается любой датой внутри него (фронт шлет date_filter).

        Args:
            date_filter: Any date inside the requested month / Любая дата внутри месяца.

        Returns:
            list[LessonResponse]: Lessons of the month / Уроки месяца.
        """
        ...

    async def get_month_schedule(self, target_date: date) -> ScheduleResponse:
        """
        Get complete schedule for a calendar month in response wrapper.

        Получить полное расписание за календарный месяц в обертке ответа.

        Args:
            target_date: Any date inside the requested month / Любая дата внутри месяца.

        Returns:
            ScheduleResponse: Complete month schedule / Полное расписание месяца.
        """
        return ScheduleResponse(lesson_list=await self.get_month_lesson_list(target_date))

    @with_auth_refresh
    @get(endpoints.SCHEDULE_BY_DATE_RANGE.value)
    async def get_range_lesson_list(
        self,
        date_start: Annotated[date, Query()],  # pyright: ignore[reportUnusedParameter]
        date_end: Annotated[date, Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> list[LessonResponse]:
        """
        Get list of lessons scheduled for a date range (inclusive).

        Получить список уроков за диапазон дат (включительно).

        Args:
            date_start: Range start / Начало диапазона.
            date_end: Range end / Конец диапазона.

        Returns:
            list[LessonResponse]: Lessons of the range / Уроки диапазона.
        """
        ...

    async def get_range_schedule(self, date_start: date, date_end: date) -> ScheduleResponse:
        """
        Get complete schedule for a date range in response wrapper.

        Получить полное расписание за диапазон дат в обертке ответа.

        Args:
            date_start: Range start / Начало диапазона.
            date_end: Range end / Конец диапазона.

        Returns:
            ScheduleResponse: Complete range schedule / Полное расписание диапазона.
        """
        return ScheduleResponse(lesson_list=await self.get_range_lesson_list(date_start, date_end))

    @with_auth_refresh
    @get(endpoints.SCHEDULE_MONTH_EVENTS.value)
    async def get_month_event_list(
        self,
        date_filter: Annotated[date, Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> list[MonthEventResponse]:
        """
        Get list of month events for a calendar month.

        Получить список событий календарного месяца.

        Args:
            date_filter: Any date inside the requested month / Любая дата внутри месяца.

        Returns:
            list[MonthEventResponse]: Month events / События месяца.
        """
        ...

    async def get_month_events(self, target_date: date) -> MonthEventsResponse:
        """
        Get month events in response wrapper.

        Получить события месяца в обертке ответа.

        Args:
            target_date: Any date inside the requested month / Любая дата внутри месяца.

        Returns:
            MonthEventsResponse: Month events object / Объект событий месяца.
        """
        return MonthEventsResponse(month_event_list=await self.get_month_event_list(target_date))
