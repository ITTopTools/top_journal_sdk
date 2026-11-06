"""Live-тесты TopJournalSDKV2 (journalka.top-academy.ru).

Требуют TOP_JOURNAL_USERNAME/PASSWORD в env или `.env`, иначе скипаются.
Марка: live (`uv run pytest -m live`).
"""

import os

import pytest

from top_journal_sdk import TopJournalSDKV2
from top_journal_sdk.v2.models.auth import RefreshResponse

_LIVE_CREDS = bool(
    os.environ.get("TOP_JOURNAL_USERNAME") and os.environ.get("TOP_JOURNAL_PASSWORD")
)

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not _LIVE_CREDS, reason="live creds missing"),
]


def _username() -> str:
    return os.environ["TOP_JOURNAL_USERNAME"]


def _password() -> str:
    return os.environ["TOP_JOURNAL_PASSWORD"]


async def test_live_login_and_cookies() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        data = await sdk.login(_username(), _password())
        assert data.user_type == 1
        assert data.user_role == "student"

        cookies = dict(sdk.client.cookies)
        assert "journal_access_token" in cookies
        assert "journal_refresh_token" in cookies


async def test_live_user_info() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        info = await sdk.user.get_personal_info()
        assert info.user.id > 0
        assert info.user.full_name
        assert info.user.current_group_id > 0


async def test_live_dashboard_endpoints() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())

        # Публичные (без __ddg*)
        langs = await sdk.client.get("/api/public/languages")
        assert langs.status_code == 200
        assert "languages" in langs.json()

        translations = await sdk.client.get("/api/public/translations")
        assert translations.status_code == 200
        assert "translations" in translations.json()

        # Dashboard
        attendance = await sdk.dashboard.get_home_attendance()
        assert isinstance(attendance.items, list)

        progress = await sdk.dashboard.get_home_average_progress()
        assert isinstance(progress.items, list)

        activity = await sdk.dashboard.get_home_activity()
        assert isinstance(activity.items, list)

        stats = await sdk.dashboard.get_stats_homework()
        assert stats.homework_total >= 0

        counters = await sdk.dashboard.get_stats_page_counters()
        assert counters.announcements_unread >= 0

        stories = await sdk.dashboard.get_stories()
        assert isinstance(stories.items, list)


async def test_live_schedule_with_dates() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        schedule = await sdk.dashboard.get_schedule(
            scope="week",
            date_start="2026-10-19",
            date_end="2026-10-25",
        )
        assert isinstance(schedule.items, list)


async def test_live_logout() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        assert await sdk.logout() is True


async def test_live_auth_refresh() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        response = await sdk.auth.refresh()
        assert isinstance(response, RefreshResponse)
        assert response.ok is True


async def test_live_home_leaderboards() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())

        group = await sdk.dashboard.get_home_leader_group()
        assert isinstance(group.items, list)

        group_points = await sdk.dashboard.get_home_leader_group_points()
        assert group_points.student_position >= 0

        stream = await sdk.dashboard.get_home_leader_stream()
        assert isinstance(stream.items, list)

        stream_points = await sdk.dashboard.get_home_leader_stream_points()
        assert stream_points.student_position >= 0

        reviews = await sdk.dashboard.get_home_reviews_count()
        assert reviews.reviews_count >= 0

        achievements = await sdk.dashboard.get_home_achievements_count()
        assert achievements.active_achievements_count >= 0


async def test_live_future_exams() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        exams = await sdk.dashboard.get_home_future_exams()
        assert isinstance(exams.items, list)


async def test_live_lesson_evaluations() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        data = await sdk.dashboard.get_lesson_evaluations()
        assert isinstance(data, dict)


async def test_live_profile_documents() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())

        settings = await sdk.profile.get_settings()
        assert settings.profile.id > 0

        documents = await sdk.profile.get_documents(student_id=settings.profile.id)
        assert isinstance(documents.documents.has_any_data, bool)

        fields = await sdk.profile.get_documents_fields(student_id=settings.profile.id)
        assert isinstance(fields, dict)


async def test_live_startup_endpoints() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())

        cc = await sdk.dashboard.get_startup_check_cancellation()
        assert cc.status == 204

        ec = await sdk.dashboard.get_startup_email_confirmation()
        assert ec.email_confirmation is None

        le = await sdk.dashboard.get_startup_lesson_evaluations()
        assert le.lesson_evaluation_pending_count >= 0

        oi = await sdk.dashboard.get_startup_opened_interview()
        assert oi.opened_interview is None

        signals = await sdk.dashboard.get_startup_signals()
        assert isinstance(signals.signals_list, list)

        # delay-email-confirmation и delay-interview требуют исследования
        # формата запроса (вероятно, POST с телом), поэтому не тестируем в лайве.


async def test_live_stats_materials_support() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())

        materials = await sdk.dashboard.get_stats_materials()
        assert materials.materials_total >= 0

        support = await sdk.dashboard.get_stats_support()
        assert support.support_unread >= 0


async def test_live_support_requests() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        await sdk.login(_username(), _password())
        requests = await sdk.dashboard.get_support_requests()
        assert isinstance(requests, list)
