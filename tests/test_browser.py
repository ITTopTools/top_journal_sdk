# pyright: reportPrivateUsage=false
"""Regression coverage for browser login and blocked HTTP requests."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from top_journal_sdk.browser import BrowserFallbackClient


@pytest.mark.parametrize("status", [200, 401, 403, 429, 500])
async def test_browser_fallback_statuses(status: int, monkeypatch: pytest.MonkeyPatch) -> None:
    browser = AsyncMock(return_value=httpx.Response(200, json={"userType": 1}))
    monkeypatch.setattr(BrowserFallbackClient, "_request_in_browser", browser)
    async with BrowserFallbackClient(
        browser_base_url="https://journalka.top-academy.ru",
        transport=httpx.MockTransport(lambda _: httpx.Response(status, json={})),
    ) as client:
        response = await client.post(
            "https://journalka.top-academy.ru/api/auth/login",
            json={
                "username": "test",
                "password": "secret",
            },
        )
        if status in {403, 429}:
            assert response.json() == {"userType": 1}
            request = browser.call_args.args[0]
            assert request.method == "POST"
            assert b'"password":"secret"' in request.content
            browser.assert_awaited_once()
        else:
            assert response.status_code == status
            browser.assert_not_awaited()


async def test_html_challenge_and_opt_out(monkeypatch: pytest.MonkeyPatch) -> None:
    browser = AsyncMock(return_value=httpx.Response(200, json={}))
    monkeypatch.setattr(BrowserFallbackClient, "_request_in_browser", browser)
    for enabled in (True, False):
        async with BrowserFallbackClient(
            browser_base_url="https://example.test",
            browser_fallback=enabled,
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    200, text="<html>DDoS-Guard</html>", headers={"content-type": "text/html"}
                )
            ),
        ) as client:
            await client.get("https://example.test/api")
    browser.assert_awaited_once()


async def test_connect_failure_uses_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    browser = AsyncMock(return_value=httpx.Response(200, json={}))
    monkeypatch.setattr(BrowserFallbackClient, "_request_in_browser", browser)

    def handler(request: httpx.Request) -> httpx.Response:
        message = "connect timed out"
        raise httpx.ConnectTimeout(message, request=request)

    async with BrowserFallbackClient(
        browser_base_url="https://example.test", transport=httpx.MockTransport(handler)
    ) as client:
        assert (await client.get("https://example.test/api")).status_code == 200
    browser.assert_awaited_once()


@pytest.mark.parametrize("failure", ["", "fetch"])
async def test_browser_login_copies_session(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    api = pytest.importorskip("playwright.async_api")
    page = MagicMock()
    page.goto = AsyncMock(return_value=None)
    page.wait_for_function = AsyncMock()
    page.evaluate = AsyncMock(
        return_value={
            "status": 200,
            "headers": {"content-type": "application/json", "content-encoding": "gzip"},
            "body": '{"userType":1,"userRole":"student"}',
        }
    )
    if failure:
        page.evaluate.side_effect = api.Error("fetch failed")
    context = MagicMock()
    context.add_cookies = AsyncMock()
    context.new_page = AsyncMock(return_value=page)
    context.cookies = AsyncMock(
        return_value=[
            {
                "name": "journal_access_token",
                "value": "NEW",
                "domain": "example.test",
                "path": "/",
                "secure": True,
                "httpOnly": True,
                "expires": -1,
            }
        ]
    )
    browser = MagicMock()
    browser.new_context = AsyncMock(return_value=context)
    browser.close = AsyncMock()
    playwright = MagicMock()
    playwright.chromium.launch = AsyncMock(return_value=browser)
    manager = MagicMock()
    manager.__aenter__ = AsyncMock(return_value=playwright)
    manager.__aexit__ = AsyncMock(return_value=False)
    monkeypatch.setattr(api, "async_playwright", lambda: manager)
    async with BrowserFallbackClient(
        browser_base_url="https://example.test",
        transport=httpx.MockTransport(lambda _: httpx.Response(403)),
    ) as client:
        if failure:
            with pytest.raises(RuntimeError, match="Browser recovery failed"):
                await client.post("https://example.test/login", json={"password": "secret"})
        else:
            response = await client.post("https://example.test/login", json={"password": "secret"})
            assert response.json()["userRole"] == "student"
            assert client.cookies.get("journal_access_token") == "NEW"
            cookie = next(iter(client.cookies.jar))
            assert cookie.secure
            assert cookie.has_nonstandard_attr("HttpOnly")
    browser.close.assert_awaited_once()
    assert page.evaluate.call_args.args[1]["body"] == '{"password":"secret"}'


async def test_v2_protected_401_uses_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    from top_journal_sdk import TopJournalSDKV2

    browser = AsyncMock(
        return_value=httpx.Response(
            200,
            json={"items": []},
            request=httpx.Request("GET", "https://journalka.top-academy.ru/api"),
        )
    )
    monkeypatch.setattr(BrowserFallbackClient, "_request_in_browser", browser)
    async with TopJournalSDKV2() as sdk:
        sdk.client._transport = httpx.MockTransport(lambda _: httpx.Response(401, json={}))
        result = await sdk.dashboard.get_home_attendance()
        assert result.items == []
    browser.assert_awaited_once()


async def test_missing_browser_has_install_instructions(monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util

    def missing_spec(_name: str) -> None:
        return None

    monkeypatch.setattr(importlib.util, "find_spec", missing_spec)
    async with BrowserFallbackClient(
        browser_base_url="https://example.test",
        transport=httpx.MockTransport(lambda _: httpx.Response(403)),
    ) as client:
        with pytest.raises(RuntimeError, match="playwright install chromium"):
            await client.get("https://example.test")
