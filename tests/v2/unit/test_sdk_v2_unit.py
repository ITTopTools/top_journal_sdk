# pyright: reportPrivateUsage=false
"""Unit-тесты TopJournalSDKV2 (без сети)."""

from __future__ import annotations

import httpx
import pytest

from top_journal_sdk.v2.client import TopJournalSDKV2

_BASE_URL = "https://journalka.top-academy.ru"


def test_v2_initialization_without_network() -> None:
    sdk = TopJournalSDKV2(timeout=5.0, auto_refresh_ddg=False)
    assert sdk._client is None
    assert sdk._ddg.has_cookies is False
    assert sdk._ddg.should_auto_refresh() is False


def test_v2_ddg_cookies_passed() -> None:
    sdk = TopJournalSDKV2(
        timeout=5.0,
        ddg_cookies={"__ddg1_": "manual"},
        auto_refresh_ddg=False,
    )
    assert sdk._ddg.cookies == {"__ddg1_": "manual"}
    assert sdk._ddg.has_cookies is True


def test_v2_client_requires_initialization() -> None:
    sdk = TopJournalSDKV2(auto_refresh_ddg=False)
    with pytest.raises(RuntimeError, match="not initialized"):
        _ = sdk.client


def test_v2_controllers_are_cached() -> None:
    sdk = TopJournalSDKV2(auto_refresh_ddg=False)
    assert sdk.auth is sdk.auth
    assert sdk.user is sdk.user
    assert sdk.dashboard is sdk.dashboard
    assert sdk.profile is sdk.profile


@pytest.mark.asyncio
async def test_v2_retries_request_after_auth_refresh() -> None:
    user_info_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal user_info_calls
        if request.url.path == "/api/auth/refresh":
            return httpx.Response(
                200,
                json={"ok": True},
                headers={
                    "set-cookie": (
                        "journal_access_token=NEW; Path=/; Domain=journalka.top-academy.ru"
                    )
                },
            )
        user_info_calls += 1
        if user_info_calls == 1:
            return httpx.Response(401, json={"detail": "expired"})
        return httpx.Response(
            200,
            json={
                "user": {
                    "id": 1,
                    "fullName": "A B",
                    "groupName": "G",
                    "currentGroupId": 9,
                    "groups": [],
                    "streamName": "S",
                }
            },
        )

    sdk = TopJournalSDKV2(auto_refresh_ddg=False)
    client = httpx.AsyncClient(
        base_url=_BASE_URL,
        transport=httpx.MockTransport(handler),
    )
    client.cookies.set("journal_refresh_token", "R", domain="journalka.top-academy.ru")
    sdk._client = client

    try:
        info = await sdk.user.get_personal_info()
    finally:
        await sdk.close()

    assert info.user.id == 1
    assert user_info_calls == 2


async def test_auth_cookie_attributes_and_deletion() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/auth/login":
            return httpx.Response(
                200,
                json={"userType": 1, "userRole": "student"},
                headers={"set-cookie": "journal_access_token=A; Path=/; Secure; HttpOnly"},
            )
        if request.url.path == "/api/auth/refresh":
            return httpx.Response(
                200,
                json={"ok": True},
                headers={"set-cookie": "journal_access_token=; Path=/; Max-Age=0"},
            )
        return httpx.Response(200, json={})

    sdk = TopJournalSDKV2(auto_refresh_ddg=False)
    sdk._client = httpx.AsyncClient(base_url=_BASE_URL, transport=httpx.MockTransport(handler))
    async with sdk:
        await sdk.login("u", "p")
        cookies = list(sdk.client.cookies.jar)
        assert len(cookies) == 1
        assert cookies[0].secure is True
        assert cookies[0].domain_specified is False
        await sdk.refresh()
        assert "journal_access_token" not in sdk.client.cookies
        sdk.client.cookies.set("journal_refresh_token", "R", domain="journalka.top-academy.ru")
        sdk.set_ddg_cookies({"__ddg1_": "D"})
        assert await sdk.logout()
        assert "journal_refresh_token" not in sdk.client.cookies
        assert sdk.client.cookies.get("__ddg1_") == "D"


@pytest.mark.parametrize("refresh_status", [200, 401, 500])
async def test_failed_refresh_does_not_retry_forever(refresh_status: int) -> None:
    paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/api/auth/refresh":
            return httpx.Response(refresh_status, json={"ok": False})
        return httpx.Response(401, json={})

    sdk = TopJournalSDKV2(auto_refresh_ddg=False)
    sdk._client = httpx.AsyncClient(base_url=_BASE_URL, transport=httpx.MockTransport(handler))
    async with sdk:
        sdk.client.cookies.set("journal_refresh_token", "R")
        response = await sdk.get("/protected")
        assert response.status_code == 401
    assert paths == ["/protected", "/api/auth/refresh"]


async def test_concurrent_requests_share_refresh() -> None:
    import asyncio

    initial_requests = 0
    refreshes = 0
    ready = asyncio.Event()

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal initial_requests, refreshes
        if request.url.path == "/api/auth/refresh":
            refreshes += 1
            await asyncio.sleep(0)
            return httpx.Response(
                200,
                json={"ok": True},
                headers={"set-cookie": "journal_access_token=NEW; Path=/"},
            )
        if "journal_access_token=NEW" in request.headers.get("cookie", ""):
            return httpx.Response(200, json={})
        initial_requests += 1
        if initial_requests == 2:
            ready.set()
        await asyncio.wait_for(ready.wait(), timeout=2)
        return httpx.Response(401, json={})

    sdk = TopJournalSDKV2(auto_refresh_ddg=False)
    sdk._client = httpx.AsyncClient(base_url=_BASE_URL, transport=httpx.MockTransport(handler))
    async with sdk:
        sdk.client.cookies.set("journal_refresh_token", "R")
        responses = await asyncio.gather(sdk.get("/protected"), sdk.get("/protected"))
        assert all(response.status_code == 200 for response in responses)
    assert refreshes == 1


@pytest.mark.parametrize("browser_fails", [False, True])
async def test_ddg_recovery(monkeypatch: pytest.MonkeyPatch, *, browser_fails: bool) -> None:
    from unittest.mock import AsyncMock

    from top_journal_sdk.v2.ddg import DdgCookieManager

    def handler(request: httpx.Request) -> httpx.Response:
        if "__ddg1_=NEW" in request.headers.get("cookie", ""):
            return httpx.Response(200, json={})
        return httpx.Response(401, json={})

    sdk = TopJournalSDKV2()
    sdk._client = httpx.AsyncClient(base_url=_BASE_URL, transport=httpx.MockTransport(handler))
    sdk.ddg._playwright_available = True

    async def refresh() -> None:
        sdk.set_ddg_cookies({"__ddg1_": "NEW"})

    browser = AsyncMock(
        side_effect=RuntimeError("browser unavailable") if browser_fails else refresh
    )
    monkeypatch.setattr(DdgCookieManager, "refresh_via_playwright", browser)
    async with sdk:
        response = await sdk.get("/protected")
        assert response.status_code == (401 if browser_fails else 200)
    browser.assert_awaited_once()
