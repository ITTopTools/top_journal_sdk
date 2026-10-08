"""Live-тесты Волны 1: парсинг реальных ответов API в модели SDK.

Требуют TOP_JOURNAL_USERNAME/PASSWORD в env, иначе скипаются.
Марка: live (uv run pytest -m live).
"""

import os
from datetime import date

import pytest

from top_journal_sdk import TopJournalSDK

_LIVE_CREDS = bool(
    os.environ.get("TOP_JOURNAL_USERNAME") and os.environ.get("TOP_JOURNAL_PASSWORD")
)

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not _LIVE_CREDS, reason="live creds missing"),
]


async def _login() -> TopJournalSDK:
    sdk = TopJournalSDK(timeout=30.0)
    await sdk.initialize()
    await sdk.login(os.environ["TOP_JOURNAL_USERNAME"], os.environ["TOP_JOURNAL_PASSWORD"])
    return sdk


async def test_live_schedule_month_range_events() -> None:
    sdk = await _login()
    try:
        month = await sdk.schedule.get_month_schedule(date(2026, 9, 1))
        assert len(month.lesson_list) > 0
        assert month.lesson_list[0].subject_name

        month_range = await sdk.schedule.get_range_schedule(date(2026, 9, 1), date(2026, 9, 7))
        assert len(month_range.lesson_list) > 0

        events = await sdk.schedule.get_month_events(date(2026, 10, 1))
        assert isinstance(events.month_event_list, list)
    finally:
        await sdk.close()


async def test_live_homework_wave1() -> None:
    sdk = await _login()
    try:
        page = await sdk.homework.get_homeworks_list()
        assert len(page.homework_list) > 0
        assert page.homework_list[0].id > 0

        tags = await sdk.homework.get_homework_tags()
        assert len(tags.homework_tag_list) > 0

        history = await sdk.homework.get_group_histories()
        assert len(history.group_history_list) > 0
    finally:
        await sdk.close()


async def test_live_dashboard() -> None:
    sdk = await _login()
    try:
        charts = await sdk.dashboard.get_progress_charts()
        assert isinstance(charts.progress_chart_list, list)

        exams = await sdk.dashboard.get_future_exams()
        assert isinstance(exams.future_exam_list, list)

        perf = await sdk.dashboard.get_academic_performance()
        assert perf.max_allowed_point > 0

        activities = await sdk.dashboard.get_activities()
        assert isinstance(activities.activity_list, list)

        stat = await sdk.dashboard.get_attendance_statistic()
        assert stat.stat_total >= 0

        group_points = await sdk.dashboard.get_leader_group_points()
        assert group_points.student_position > 0

        stream_points = await sdk.dashboard.get_leader_stream_points()
        assert stream_points.student_position > 0

        counters = await sdk.dashboard.get_page_counters()
        assert isinstance(counters.page_counter_list, list)
    finally:
        await sdk.close()


async def test_live_exams() -> None:
    sdk = await _login()
    try:
        exams = await sdk.exams.get_student_exams()
        assert isinstance(exams.student_exam_list, list)

        quarterly = await sdk.exams.get_quarterly_grades()
        assert isinstance(quarterly.grades, list)
    finally:
        await sdk.close()
