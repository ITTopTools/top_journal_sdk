# pyright: reportPrivateUsage=false
"""Мокированные unit-тесты контроллеров v2 (без сети)."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from top_journal_sdk.v2.client import TopJournalSDKV2
from top_journal_sdk.v2.controllers.auth import AuthController
from top_journal_sdk.v2.controllers.dashboard import DashboardController
from top_journal_sdk.v2.controllers.profile import ProfileController
from top_journal_sdk.v2.enums.endpoints import JournalkaEndpoints as endpoints


def _make_sdk() -> tuple[TopJournalSDKV2, MagicMock]:
    sdk = TopJournalSDKV2(timeout=5.0, auto_refresh_ddg=False)
    client = MagicMock(spec=httpx.AsyncClient)
    sdk._client = client
    return sdk, client


def _json_response(payload: object) -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = payload
    return response


async def _call_endpoint(controller: object, method: str) -> object:
    endpoint = cast(Callable[[], Awaitable[object]], getattr(controller, method))
    return await endpoint()


@pytest.mark.asyncio
async def test_auth_login() -> None:
    sdk, _ = _make_sdk()
    ctrl = AuthController(sdk)

    resp = MagicMock()
    resp.status_code = 200
    resp.cookies = MagicMock()
    resp.cookies.items.return_value = [
        ("journal_access_token", "AT"),
        ("journal_refresh_token", "RT"),
        ("journal_user_type", "1"),
        ("journal_user_role", "student"),
    ]
    resp.json.return_value = {"userType": 1, "userRole": "student"}
    sdk.post = AsyncMock(return_value=resp)

    result = await ctrl.login("user", "pass")

    assert result.user_type == 1
    assert result.user_role == "student"
    sdk.post.assert_called_once_with(
        endpoints.AUTH_LOGIN.value,
        json={"username": "user", "password": "pass"},
        refresh_on_401=False,
    )


@pytest.mark.asyncio
async def test_auth_logout() -> None:
    sdk, _ = _make_sdk()
    ctrl = AuthController(sdk)

    resp = MagicMock()
    resp.status_code = 200
    resp.is_success = True
    sdk.post = AsyncMock(return_value=resp)

    assert await ctrl.logout() is True
    sdk.post.assert_called_once_with(endpoints.AUTH_LOGOUT.value, refresh_on_401=False)


@pytest.mark.asyncio
async def test_auth_refresh() -> None:
    sdk, _ = _make_sdk()
    ctrl = AuthController(sdk)

    resp = MagicMock()
    resp.status_code = 200
    resp.cookies = {"journal_access_token": "NEW_AT"}
    resp.json.return_value = {"ok": True}
    sdk.post = AsyncMock(return_value=resp)

    result = await ctrl.refresh()
    assert result.ok is True
    sdk.post.assert_called_once_with(endpoints.AUTH_REFRESH.value, refresh_on_401=False)


@pytest.mark.asyncio
async def test_dashboard_home_attendance() -> None:
    sdk, _ = _make_sdk()
    ctrl = DashboardController(sdk)

    sdk.get = AsyncMock(
        return_value=_json_response({"items": [{"date": "2026-10-01", "points": 100}]})
    )

    result = await ctrl.get_home_attendance()
    assert result.items[0].points == 100
    sdk.get.assert_called_once_with(endpoints.HOME_ATTENDANCE.value)


@pytest.mark.asyncio
async def test_dashboard_startup_signals() -> None:
    sdk, _ = _make_sdk()
    ctrl = DashboardController(sdk)

    sdk.get = AsyncMock(return_value=_json_response({"signalsList": []}))

    result = await ctrl.get_startup_signals()
    assert result.signals_list == []


@pytest.mark.asyncio
async def test_dashboard_stories_lead_post() -> None:
    sdk, _ = _make_sdk()
    ctrl = DashboardController(sdk)

    sdk.post = AsyncMock(return_value=_json_response({}))

    result = await ctrl.get_stories_lead()
    assert result.id is None
    sdk.post.assert_called_once_with(endpoints.STORIES_LEAD.value, json={})


@pytest.mark.asyncio
async def test_dashboard_support_requests_list() -> None:
    sdk, _ = _make_sdk()
    ctrl = DashboardController(sdk)

    sdk.get = AsyncMock(return_value=_json_response([{"id": 1, "title": "Test"}]))

    result = await ctrl.get_support_requests()
    assert result == [{"id": 1, "title": "Test"}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path,payload",
    [
        ("get_home_activity", endpoints.HOME_ACTIVITY.value, {"items": []}),
        ("get_home_average_progress", endpoints.HOME_AVERAGE_PROGRESS.value, {"items": []}),
        ("get_home_future_exams", endpoints.HOME_FUTURE_EXAMS.value, {"items": []}),
        ("get_home_leader_group", endpoints.HOME_LEADER_GROUP.value, {"items": []}),
        ("get_home_leader_stream", endpoints.HOME_LEADER_STREAM.value, {"items": []}),
        ("get_home_reviews_count", endpoints.HOME_REVIEWS_COUNT.value, {"reviews_count": 0}),
        (
            "get_home_achievements_count",
            endpoints.HOME_ACHIEVEMENTS_COUNT.value,
            {"active_achievements_count": 0},
        ),
        ("get_lesson_evaluations", endpoints.LESSON_EVALUATIONS.value, {}),
        (
            "get_startup_check_cancellation",
            endpoints.STARTUP_CHECK_CANCELLATION.value,
            {"status": 204, "is_cancellation_active": False},
        ),
        ("get_startup_signals", endpoints.STARTUP_SIGNALS.value, {"signals_list": []}),
        (
            "get_stats_homework",
            endpoints.STATS_HOMEWORK.value,
            {"homework_total": 0, "homework_new": 0},
        ),
        (
            "get_stats_page_counters",
            endpoints.STATS_PAGE_COUNTERS.value,
            {
                "announcements_unread": 0,
                "reviews_unread": 0,
                "materials_new": 0,
                "vacancy_unread": 0,
                "signal_unread": 0,
                "profile_unread": 0,
            },
        ),
        ("get_stories", endpoints.STORIES.value, {"items": []}),
        (
            "get_startup_email_confirmation",
            endpoints.STARTUP_EMAIL_CONFIRMATION.value,
            {"email_confirmation": None},
        ),
        (
            "get_startup_opened_interview",
            endpoints.STARTUP_OPENED_INTERVIEW.value,
            {"opened_interview": None},
        ),
        (
            "get_startup_lesson_evaluations",
            endpoints.STARTUP_LESSON_EVALUATIONS.value,
            {"lesson_evaluation_pending_count": 0},
        ),
    ],
)
async def test_dashboard_get_endpoints(method: str, path: str, payload: dict[str, Any]) -> None:
    sdk, _ = _make_sdk()
    ctrl = DashboardController(sdk)

    sdk.get = AsyncMock(return_value=_json_response(payload))

    result = await _call_endpoint(ctrl, method)
    assert result is not None
    sdk.get.assert_called_once_with(path)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path,payload",
    [
        (
            "get_settings",
            endpoints.PROFILE_SETTINGS.value,
            {
                "profile": {
                    "id": 1,
                    "full_name": "Test",
                    "first_name": "Test",
                    "last_name": "User",
                    "patronymic": "",
                    "avatar": None,
                    "level": 0,
                    "fill_percentage": 0,
                    "is_completed": False,
                    "email": None,
                    "phone": None,
                    "phones": [],
                    "birth_date": None,
                    "address": None,
                    "study": None,
                    "azure_login": None,
                    "form_type": 0,
                    "is_email_verified": False,
                    "is_phone_verified": False,
                    "has_pending_data": False,
                    "has_pending_photo": False,
                    "last_approving_status": 0,
                    "decline_comment": None,
                    "social_links": [],
                    "payment": {"has_any_data": False},
                },
            },
        ),
    ],
)
async def test_profile_get_endpoints(method: str, path: str, payload: dict[str, Any]) -> None:
    sdk, _ = _make_sdk()
    ctrl = ProfileController(sdk)

    sdk.get = AsyncMock(return_value=_json_response(payload))

    result = await _call_endpoint(ctrl, method)
    assert result is not None
    sdk.get.assert_called_once_with(path)


@pytest.mark.asyncio
async def test_profile_change_group() -> None:
    sdk, _ = _make_sdk()
    ctrl = ProfileController(sdk)

    sdk.post = AsyncMock(return_value=_json_response({"ok": True}))

    result = await ctrl.change_group(9)
    assert result == {"ok": True}
    sdk.post.assert_called_once_with(endpoints.GROUPS_CHANGE.value, json={"groupId": 9})
