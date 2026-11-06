"""Мокированные unit-тесты DdG cookie manager (без Playwright)."""

import pytest

from top_journal_sdk.v2.ddg import DDG_COOKIE_NAMES, DdgCookieManager


def test_ddg_empty_by_default() -> None:
    m = DdgCookieManager()
    assert m.has_cookies is False
    assert m.cookies == {}


def test_ddg_set_and_get() -> None:
    m = DdgCookieManager()
    m.set_ddg_cookies(
        {
            "__ddg1_": "aaa",
            "__ddg8_": "bbb",
            "__ddg9_": "ccc",
            "__ddg10_": "ddd",
            "journal_access_token": "ignored",
        }
    )
    assert m.has_cookies is True
    for name in DDG_COOKIE_NAMES:
        assert name in m.cookies
    assert "journal_access_token" not in m.cookies

    header = m.get_cookie_header()
    assert "__ddg1_=aaa" in header
    assert "__ddg10_=ddd" in header
    assert "journal_access_token" not in header


def test_ddg_merge_existing() -> None:
    m = DdgCookieManager()
    m.set_ddg_cookies({"__ddg1_": "first"})
    m.set_ddg_cookies({"__ddg8_": "second"})
    assert m.cookies == {"__ddg1_": "first", "__ddg8_": "second"}
    assert "__ddg9_" not in m.cookies


def test_ddg_preserves_new_challenge_cookies() -> None:
    manager = DdgCookieManager()
    manager.set_ddg_cookies(
        {
            "__ddgid_": "id",
            "__ddg5_": "challenge",
            "ddg_last_challenge": "last",
            "journal_refresh_token": "ignored",
        }
    )
    assert manager.cookies == {
        "__ddgid_": "id",
        "__ddg5_": "challenge",
        "ddg_last_challenge": "last",
    }


async def test_browser_cookie_collection_and_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    from unittest.mock import AsyncMock, MagicMock

    api = pytest.importorskip("playwright.async_api")
    page = MagicMock()
    page.goto = AsyncMock(side_effect=[None, api.Error("dashboard unavailable")])
    page.wait_for_timeout = AsyncMock()
    context = MagicMock()
    context.new_page = AsyncMock(return_value=page)
    context.cookies = AsyncMock(
        return_value=[
            {"name": "__ddgid_", "value": "challenge"},
            {"name": "journal_access_token", "value": "ignored"},
        ]
    )
    browser = MagicMock()
    browser.new_context = AsyncMock(return_value=context)
    browser.close = AsyncMock()
    playwright = MagicMock()
    playwright.chromium.launch = AsyncMock(return_value=browser)
    manager_context = MagicMock()
    manager_context.__aenter__ = AsyncMock(return_value=playwright)
    manager_context.__aexit__ = AsyncMock(return_value=False)
    monkeypatch.setattr(api, "async_playwright", lambda: manager_context)
    manager = DdgCookieManager()
    await manager.refresh_via_playwright()
    assert manager.cookies == {"__ddgid_": "challenge"}
    browser.close.assert_awaited_once()
