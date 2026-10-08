"""Тесты сниппетов README: python-блоки выполняются на моках.

Гарантирует, что примеры в README (страница PyPI-пакета) рабочие:
соврал в примере — упал тест. Сети нет, креды не нужны.
"""

import pathlib
import re
from typing import Any

import httpx
import pytest

import top_journal_sdk

HTML = '<html><head><script src="/s/app.1.js"></script></head></html>'
JS = 'o.authModel = new r.AuthModel("K");'
TOKENS: dict[str, str] = {"access_token": "A", "refresh_token": "R"}
USER: dict[str, object] = {
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

_JOURNAL_HOST = "journal.top-academy.ru"


def _handler(request: httpx.Request) -> httpx.Response:
    host = request.url.host
    path = request.url.path
    if host == _JOURNAL_HOST:
        if path.endswith(".js"):
            return httpx.Response(200, text=JS)
        return httpx.Response(200, text=HTML)
    if request.method == "POST" and path.endswith("/auth/login"):
        return httpx.Response(200, json=TOKENS)
    if path.endswith("/settings/user-info"):
        return httpx.Response(200, json=USER)
    if path.endswith("/schedule/operations/get-by-date"):
        return httpx.Response(200, json=SCHEDULE)
    if path.endswith("/count/homework"):
        return httpx.Response(200, json=COUNTERS)
    if path.endswith("/dashboard/progress/academic-performance"):
        return httpx.Response(200, json=PERFORMANCE)
    return httpx.Response(404, json={"detail": "unexpected"})


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
    monkeypatch.setattr(top_journal_sdk, "AsyncClient", _mocked_async_client)
    exec(compile(snippet, "<readme>", "exec"), {"__name__": "__readme__"})
