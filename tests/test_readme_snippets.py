"""Тесты сниппетов README: python-блоки выполняются на моках.

Гарантирует, что примеры в README (страница PyPI-пакета) рабочие:
соврал в примере — упал тест. Сети нет, креды не нужны.
"""

import pathlib
import re
from typing import Any

import httpx
import pytest

HTML = '<html><head><script src="/s/app.1.js"></script></head></html>'
JS = 'o.authModel = new r.AuthModel("K");'
TOKENS: dict[str, str] = {"access_token": "A", "refresh_token": "R"}
SCHEDULE: list[dict[str, object]] = [
    {
        "date": "2026-10-08",
        "lesson": 1,
        "started_at": "08:00:00",
        "finished_at": "09:35:00",
        "teacher_name": "T",
        "subject_name": "S",
        "room_name": "R",
    }
]
COUNTERS: list[dict[str, int]] = [{"counter_type": 4, "counter": 5}]
PERFORMANCE: dict[str, object] = {
    "diffMonth": 1,
    "totalMonth": 80,
    "totalAllTime": 75.5,
    "maxAllowedPoint": 100,
    "progress": {"homework": 90.0, "total": 80.0},
}

USER_V1: dict[str, object] = {
    "gaming_points": [],
    "student_id": 1,
    "full_name": "A B",
    "age": 20,
    "gender": 1,
    "birthday": "2006-01-01",
    "photo": None,
    "current_group_id": 9,
    "group_name": "G",
    "current_group_status": 1,
    "stream_id": 1,
    "stream_name": "S",
    "study_form_short_name": "F",
    "achieves_count": 0,
    "registration_date": "2024-01-01T00:00:00",
    "last_date_visit": "2024-01-01T00:00:00",
}

USER_V2: dict[str, object] = {
    "id": 1,
    "full_name": "A B",
    "group_name": "G",
    "current_group_id": 9,
    "groups": [],
    "stream_name": "S",
    "avatar": None,
    "level": 0,
    "top_coin": 0,
    "top_gem": 0,
    "top_money": 0,
    "spent_top_coin": 0,
    "spent_top_gem": 0,
    "current_top_coin": 0,
    "current_top_gem": 0,
    "point_scale": 0,
    "visibility_settings": {},
}


def _handler(request: httpx.Request) -> httpx.Response:  # noqa: C901
    path = request.url.path
    host = request.url.host
    if path.endswith(".js"):
        return httpx.Response(200, text=JS)
    if host == "journal.top-academy.ru":
        if request.method == "GET":
            html_with_js = HTML.replace("</head>", f"<script>{JS}</script></head>")
            return httpx.Response(200, text=html_with_js)
        return httpx.Response(200, json={"ok": True})
    if request.method == "POST" and path.endswith("/api/auth/login"):
        return httpx.Response(200, json={"userType": 1, "userRole": "student"})
    if request.method == "POST" and path.endswith("/auth/login"):
        return httpx.Response(200, json=TOKENS)
    if path.endswith("/settings/user-info"):
        return httpx.Response(200, json=USER_V1)
    if path.endswith("/api/dashboard/user-info"):
        return httpx.Response(200, json={"user": USER_V2})
    if path.endswith("/schedule/operations/get-by-date"):
        return httpx.Response(200, json=SCHEDULE)
    if path.endswith("/api/dashboard/home/attendance"):
        return httpx.Response(200, json={"items": [{"date": "2026-10-01", "points": 100}]})
    if path.endswith("/api/dashboard/schedule"):
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "2026-10-19-1-1",
                        "date": "2026-10-19",
                        "lesson": 1,
                        "start_time": "08:00",
                        "end_time": "09:35",
                        "start_minutes": 480,
                        "end_minutes": 575,
                        "duration_minutes": 95,
                        "subject_key": "",
                        "subject_fallback": "Математика",
                        "teacher": "Иванов И.И.",
                    }
                ]
            },
        )
    if path.endswith("/count/homework"):
        return httpx.Response(200, json=COUNTERS)
    if path.endswith("/dashboard/progress/academic-performance"):
        return httpx.Response(200, json=PERFORMANCE)
    return httpx.Response(
        404,
        json={"detail": f"unexpected request: {request.method} {request.url}"},
    )


_real_async_client = httpx.AsyncClient


def _mocked_async_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
    kwargs.setdefault("transport", httpx.MockTransport(_handler))
    return _real_async_client(*args, **kwargs)


def _extract_snippets() -> list[str]:
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    found = re.findall(r"```python\n(.*?)```", readme.read_text(encoding="utf-8"), re.S)
    return [match for match in found if isinstance(match, str)]


_SNIPPETS = _extract_snippets()


def test_readme_has_snippets() -> None:
    assert len(_SNIPPETS) >= 2


@pytest.mark.parametrize("snippet", _SNIPPETS)
def test_readme_snippet_runs(monkeypatch: pytest.MonkeyPatch, snippet: str) -> None:
    monkeypatch.setattr(httpx, "AsyncClient", _mocked_async_client)
    exec(compile(snippet, "<readme>", "exec"), {"__name__": "__readme__"})
