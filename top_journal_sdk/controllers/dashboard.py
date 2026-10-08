from typing import Annotated

from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.dashboard import (
    AcademicProgressResponse,
    ActivitiesResponse,
    ActivityResponse,
    AttendanceStatisticResponse,
    FutureExamResponse,
    FutureExamsResponse,
    LeaderPointsResponse,
    PageCounterResponse,
    PageCountersResponse,
    ProgressChartResponse,
    ProgressChartsResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class DashboardController(BaseController):
    """
    Student dashboard controller.

    Handles retrieval of dashboard charts, activity feeds, ratings details
    and progress statistics.

    Контроллер дашборда студента.

    Обрабатывает получение графиков дашборда, ленты активности, деталей
    рейтингов и статистики прогресса.
    """

    @with_auth_refresh
    @get(endpoints.DASHBOARD_CHART_PROGRESS.value)
    async def get_progress_chart_list(self) -> list[ProgressChartResponse]:
        """
        Get progress charts.

        Получить графики прогресса.

        Returns:
            list[ProgressChartResponse]: Progress charts / Графики прогресса.
        """
        ...

    async def get_progress_charts(self) -> ProgressChartsResponse:
        """
        Get progress charts in response wrapper.

        Получить графики прогресса в обертке ответа.

        Returns:
            ProgressChartsResponse: Charts object / Объект графиков.
        """
        return ProgressChartsResponse(progress_chart_list=await self.get_progress_chart_list())

    @with_auth_refresh
    @get(endpoints.DASHBOARD_FUTURE_EXAMS.value)
    async def get_future_exam_list(self) -> list[FutureExamResponse]:
        """
        Get future exams.

        Получить будущие экзамены.

        Returns:
            list[FutureExamResponse]: Future exams / Будущие экзамены.
        """
        ...

    async def get_future_exams(self) -> FutureExamsResponse:
        """
        Get future exams in response wrapper.

        Получить будущие экзамены в обертке ответа.

        Returns:
            FutureExamsResponse: Exams object / Объект экзаменов.
        """
        return FutureExamsResponse(future_exam_list=await self.get_future_exam_list())

    @with_auth_refresh
    @get(endpoints.DASHBOARD_ACADEMIC_PERFORMANCE.value)
    async def get_academic_performance(self) -> AcademicProgressResponse:
        """
        Get academic performance summary.

        Получить сводку академической успеваемости.

        Returns:
            AcademicProgressResponse: Performance summary / Сводка успеваемости.
        """
        ...

    @with_auth_refresh
    @get(endpoints.DASHBOARD_ACTIVITY.value)
    async def get_activity_list(self) -> list[ActivityResponse]:
        """
        Get student activity feed.

        Получить ленту активности студента.

        Returns:
            list[ActivityResponse]: Activity entries / Записи активности.
        """
        ...

    async def get_activities(self) -> ActivitiesResponse:
        """
        Get student activity feed in response wrapper.

        Получить ленту активности студента в обертке ответа.

        Returns:
            ActivitiesResponse: Activities object / Объект активности.
        """
        return ActivitiesResponse(activity_list=await self.get_activity_list())

    @with_auth_refresh
    @get(endpoints.DASHBOARD_ATTENDANCE_STATISTIC.value)
    async def get_attendance_statistic(self) -> AttendanceStatisticResponse:
        """
        Get attendance statistic summary.

        Получить сводную статистику посещаемости.

        Returns:
            AttendanceStatisticResponse: Statistic summary / Сводка статистики.
        """
        ...

    @with_auth_refresh
    @get(endpoints.DASHBOARD_LEADER_GROUP_POINTS.value)
    async def get_leader_group_points(self) -> LeaderPointsResponse:
        """
        Get group leaderboard points detail.

        Получить детализацию баллов рейтинга группы.

        Returns:
            LeaderPointsResponse: Group points detail / Детализация баллов группы.
        """
        ...

    @with_auth_refresh
    @get(endpoints.DASHBOARD_LEADER_STREAM_POINTS.value)
    async def get_leader_stream_points(self) -> LeaderPointsResponse:
        """
        Get stream leaderboard points detail.

        Получить детализацию баллов рейтинга потока.

        Returns:
            LeaderPointsResponse: Stream points detail / Детализация баллов потока.
        """
        ...

    @with_auth_refresh
    @get(endpoints.DASHBOARD_PAGE_COUNTERS.value)
    async def get_page_counter_list(
        self,
        filter_type: Annotated[int | None, Query()] = None,  # pyright: ignore[reportUnusedParameter]
    ) -> list[PageCounterResponse]:
        """
        Get page counters.

        Получить счетчики страниц.

        Args:
            filter_type: Counter filter / Фильтр счетчиков.

        Returns:
            list[PageCounterResponse]: Page counters / Счетчики страниц.
        """
        ...

    async def get_page_counters(self, filter_type: int | None = None) -> PageCountersResponse:
        """
        Get page counters in response wrapper.

        Получить счетчики страниц в обертке ответа.

        Args:
            filter_type: Counter filter / Фильтр счетчиков.

        Returns:
            PageCountersResponse: Counters object / Объект счетчиков.
        """
        return PageCountersResponse(
            page_counter_list=await self.get_page_counter_list(filter_type)
        )
