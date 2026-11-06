from __future__ import annotations

from pydantic import TypeAdapter

from top_journal_sdk.v2.controllers.base import BaseController
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints
from top_journal_sdk.v2.models.evaluation import LessonEvaluationsResponse
from top_journal_sdk.v2.models.home import (
    AchievementsCountResponse,
    ActivityResponse,
    AttendanceResponse,
    FutureExamsResponse,
    LeaderGroupPointsResponse,
    LeaderGroupResponse,
    LeaderStreamPointsResponse,
    LeaderStreamResponse,
    ProgressResponse,
    ReviewsCountResponse,
)
from top_journal_sdk.v2.models.schedule import ScheduleResponse
from top_journal_sdk.v2.models.startup import (
    CheckCancellationResponse,
    DelayEmailConfirmationResponse,
    DelayInterviewResponse,
    EmailConfirmationResponse,
    LessonEvaluationPendingResponse,
    OpenedInterviewResponse,
    SignalsResponse,
)
from top_journal_sdk.v2.models.stats import (
    HomeworkStatsResponse,
    MaterialsStatsResponse,
    PageCountersResponse,
    SupportStatsResponse,
)
from top_journal_sdk.v2.models.stories import StoriesResponse, StoryLeadResponse
from top_journal_sdk.v2.models.support import SupportRequest


class DashboardController(BaseController):
    """Контроллер дашборда для journalka API v2."""

    # ----- Home -----

    async def get_home_attendance(self) -> AttendanceResponse:
        """GET /api/dashboard/home/attendance"""
        response = await self.sdk.get(endpoints.HOME_ATTENDANCE.value)
        response.raise_for_status()
        return AttendanceResponse.model_validate(response.json())

    async def get_home_average_progress(self) -> ProgressResponse:
        """GET /api/dashboard/home/average-progress"""
        response = await self.sdk.get(endpoints.HOME_AVERAGE_PROGRESS.value)
        response.raise_for_status()
        return ProgressResponse.model_validate(response.json())

    async def get_home_activity(self) -> ActivityResponse:
        """GET /api/dashboard/home/activity"""
        response = await self.sdk.get(endpoints.HOME_ACTIVITY.value)
        response.raise_for_status()
        return ActivityResponse.model_validate(response.json())

    async def get_home_future_exams(self) -> FutureExamsResponse:
        """GET /api/dashboard/home/future-exams"""
        response = await self.sdk.get(endpoints.HOME_FUTURE_EXAMS.value)
        response.raise_for_status()
        return FutureExamsResponse.model_validate(response.json())

    async def get_home_leader_group(self) -> LeaderGroupResponse:
        """GET /api/dashboard/home/leader-group"""
        response = await self.sdk.get(endpoints.HOME_LEADER_GROUP.value)
        response.raise_for_status()
        return LeaderGroupResponse.model_validate(response.json())

    async def get_home_leader_group_points(self) -> LeaderGroupPointsResponse:
        """GET /api/dashboard/home/leader-group-points"""
        response = await self.sdk.get(endpoints.HOME_LEADER_GROUP_POINTS.value)
        response.raise_for_status()
        return LeaderGroupPointsResponse.model_validate(response.json())

    async def get_home_leader_stream(self) -> LeaderStreamResponse:
        """GET /api/dashboard/home/leader-stream"""
        response = await self.sdk.get(endpoints.HOME_LEADER_STREAM.value)
        response.raise_for_status()
        return LeaderStreamResponse.model_validate(response.json())

    async def get_home_leader_stream_points(self) -> LeaderStreamPointsResponse:
        """GET /api/dashboard/home/leader-stream-points"""
        response = await self.sdk.get(endpoints.HOME_LEADER_STREAM_POINTS.value)
        response.raise_for_status()
        return LeaderStreamPointsResponse.model_validate(response.json())

    async def get_home_reviews_count(self) -> ReviewsCountResponse:
        """GET /api/dashboard/home/reviews-count"""
        response = await self.sdk.get(endpoints.HOME_REVIEWS_COUNT.value)
        response.raise_for_status()
        return ReviewsCountResponse.model_validate(response.json())

    async def get_home_achievements_count(self) -> AchievementsCountResponse:
        """GET /api/dashboard/home/achievements-count"""
        response = await self.sdk.get(endpoints.HOME_ACHIEVEMENTS_COUNT.value)
        response.raise_for_status()
        return AchievementsCountResponse.model_validate(response.json())

    # ----- Lesson evaluations -----

    async def get_lesson_evaluations(self) -> LessonEvaluationsResponse:
        """GET /api/dashboard/lesson-evaluations"""
        response = await self.sdk.get(endpoints.LESSON_EVALUATIONS.value)
        response.raise_for_status()
        return LessonEvaluationsResponse.model_validate(response.json())

    # ----- Startup -----

    async def get_startup_check_cancellation(self) -> CheckCancellationResponse:
        """GET /api/dashboard/startup/check-cancellation"""
        response = await self.sdk.get(endpoints.STARTUP_CHECK_CANCELLATION.value)
        response.raise_for_status()
        return CheckCancellationResponse.model_validate(response.json())

    async def delay_email_confirmation(self) -> DelayEmailConfirmationResponse:
        """POST /api/dashboard/startup/delay-email-confirmation (changes reminder state)."""
        response = await self.sdk.post(endpoints.STARTUP_DELAY_EMAIL_CONFIRMATION.value)
        response.raise_for_status()
        if not response.content:
            return DelayEmailConfirmationResponse()
        return DelayEmailConfirmationResponse.model_validate(response.json())

    async def delay_interview(self, interview_id: int | str) -> DelayInterviewResponse:
        """POST /api/dashboard/startup/delay-interview with the interview ID."""
        response = await self.sdk.post(
            endpoints.STARTUP_DELAY_INTERVIEW.value, json={"id": interview_id}
        )
        response.raise_for_status()
        if not response.content:
            return DelayInterviewResponse()
        return DelayInterviewResponse.model_validate(response.json())

    async def get_startup_delay_email_confirmation(self) -> DelayEmailConfirmationResponse:
        """Compatibility alias for delay_email_confirmation(); sends POST."""
        return await self.delay_email_confirmation()

    async def get_startup_delay_interview(self, interview_id: int | str) -> DelayInterviewResponse:
        """Compatibility alias for delay_interview(); sends POST."""
        return await self.delay_interview(interview_id)

    async def get_startup_email_confirmation(self) -> EmailConfirmationResponse:
        """GET /api/dashboard/startup/email-confirmation"""
        response = await self.sdk.get(endpoints.STARTUP_EMAIL_CONFIRMATION.value)
        response.raise_for_status()
        return EmailConfirmationResponse.model_validate(response.json())

    async def get_startup_lesson_evaluations(self) -> LessonEvaluationPendingResponse:
        """GET /api/dashboard/startup/lesson-evaluations"""
        response = await self.sdk.get(endpoints.STARTUP_LESSON_EVALUATIONS.value)
        response.raise_for_status()
        return LessonEvaluationPendingResponse.model_validate(response.json())

    async def get_startup_opened_interview(self) -> OpenedInterviewResponse:
        """GET /api/dashboard/startup/opened-interview"""
        response = await self.sdk.get(endpoints.STARTUP_OPENED_INTERVIEW.value)
        response.raise_for_status()
        return OpenedInterviewResponse.model_validate(response.json())

    async def get_startup_signals(self) -> SignalsResponse:
        """GET /api/dashboard/startup/signals"""
        response = await self.sdk.get(endpoints.STARTUP_SIGNALS.value)
        response.raise_for_status()
        return SignalsResponse.model_validate(response.json())

    # ----- Stats -----

    async def get_stats_homework(self) -> HomeworkStatsResponse:
        """GET /api/dashboard/stats/homework"""
        response = await self.sdk.get(endpoints.STATS_HOMEWORK.value)
        response.raise_for_status()
        return HomeworkStatsResponse.model_validate(response.json())

    async def get_stats_materials(self) -> MaterialsStatsResponse:
        """GET /api/dashboard/stats/materials"""
        response = await self.sdk.get(endpoints.STATS_MATERIALS.value)
        response.raise_for_status()
        return MaterialsStatsResponse.model_validate(response.json())

    async def get_stats_page_counters(self) -> PageCountersResponse:
        """GET /api/dashboard/stats/page-counters"""
        response = await self.sdk.get(endpoints.STATS_PAGE_COUNTERS.value)
        response.raise_for_status()
        return PageCountersResponse.model_validate(response.json())

    async def get_stats_support(self) -> SupportStatsResponse:
        """GET /api/dashboard/stats/support"""
        response = await self.sdk.get(endpoints.STATS_SUPPORT.value)
        response.raise_for_status()
        return SupportStatsResponse.model_validate(response.json())

    # ----- Stories -----

    async def get_stories(self) -> StoriesResponse:
        """GET /api/dashboard/stories"""
        response = await self.sdk.get(endpoints.STORIES.value)
        response.raise_for_status()
        return StoriesResponse.model_validate(response.json())

    async def get_stories_lead(self) -> StoryLeadResponse:
        """POST /api/dashboard/stories/lead"""
        response = await self.sdk.post(endpoints.STORIES_LEAD.value, json={})
        response.raise_for_status()
        return StoryLeadResponse.model_validate(response.json())

    # ----- Support -----

    async def get_support_requests(self) -> list[SupportRequest]:
        """GET /api/dashboard/support/requests/"""
        response = await self.sdk.get(endpoints.SUPPORT_REQUESTS.value)
        response.raise_for_status()
        return TypeAdapter(list[SupportRequest]).validate_python(response.json())

    # ----- Schedule -----

    async def get_schedule(
        self,
        scope: str = "week",
        date_start: str | None = None,
        date_end: str | None = None,
    ) -> ScheduleResponse:
        """GET /api/dashboard/schedule?scope=...&dateStart=...&dateEnd=..."""
        params: dict[str, str] = {"scope": scope}
        if date_start is not None:
            params["dateStart"] = date_start
        if date_end is not None:
            params["dateEnd"] = date_end
        response = await self.sdk.get(endpoints.SCHEDULE.value, params=params)
        response.raise_for_status()
        return ScheduleResponse.model_validate(response.json())
