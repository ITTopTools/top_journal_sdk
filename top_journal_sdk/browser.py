"""Optional browser fallback shared by both API versions."""

from __future__ import annotations

import importlib.util
from asyncio import Lock
from http.cookiejar import Cookie
from typing import Any, override

import httpx

_BROWSER_REQUIRED = (
    'DDoS-Guard requires a browser. Install "top-journal-sdk[browser]" '
    "and run `playwright install chromium`."
)
_BROWSER_FAILED = (
    "Browser recovery failed. Run `playwright install chromium` "
    "and check network access to the journal."
)
_BROWSER_TIMEOUT = "Browser timed out opening the journal or waiting for DDoS-Guard verification."


def is_browser_challenge(response: httpx.Response) -> bool:
    """Detect access blocks and HTML challenges, including ones returning HTTP 200."""
    if response.status_code in {403, 429}:
        return True
    if "html" not in response.headers.get("content-type", "").lower():
        return False
    body = response.text.lower()
    return any(marker in body for marker in ("ddos-guard", "ddos guard", "check.ddos"))


class BrowserFallbackClient(httpx.AsyncClient):
    """Use Chromium's fetch for blocked requests, then import its session cookies.

    Credentials only live in the original request body; they are never saved for
    subsequent logins. Each recovery closes the browser, including on errors.
    """

    def __init__(
        self, *, browser_base_url: str, browser_fallback: bool = True, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self._browser_base_url = browser_base_url
        self._browser_fallback = browser_fallback
        self._browser_lock = Lock()

    @override
    async def send(self, request: httpx.Request, **kwargs: Any) -> httpx.Response:
        try:
            response = await super().send(request, **kwargs)
        except (httpx.ConnectError, httpx.ConnectTimeout):
            # Connection establishment failed, so the server did not process a body.
            if not self._browser_fallback:
                raise
        else:
            if not self._browser_fallback or kwargs.get("stream", False):
                return response
            if not is_browser_challenge(response):
                return response
            await response.aclose()
        return await self.request_in_browser(request)

    async def request_in_browser(self, request: httpx.Request) -> httpx.Response:
        async with self._browser_lock:
            return await self._request_in_browser(request)

    async def _request_in_browser(self, request: httpx.Request) -> httpx.Response:
        if importlib.util.find_spec("playwright") is None:
            raise RuntimeError(_BROWSER_REQUIRED)

        from playwright.async_api import Error as PlaywrightError
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError
        from playwright.async_api import async_playwright

        await request.aread()
        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                try:
                    context = await browser.new_context(
                        user_agent=request.headers.get("user-agent", "Mozilla/5.0")
                    )
                    cookies: list[Any] = []
                    for cookie in self.cookies.jar:
                        if cookie.is_expired():
                            continue
                        item: dict[str, Any] = {
                            "name": cookie.name,
                            "value": cookie.value or "",
                            "domain": cookie.domain or request.url.host,
                            "path": cookie.path,
                            "secure": cookie.secure,
                            "httpOnly": cookie.has_nonstandard_attr("HttpOnly"),
                        }
                        if cookie.expires is not None:
                            item["expires"] = cookie.expires
                        cookies.append(item)
                    await context.add_cookies(cookies)
                    page = await context.new_page()
                    navigation = await page.goto(
                        self._browser_base_url, wait_until="domcontentloaded", timeout=30000
                    )
                    await page.wait_for_function(
                        """() => !/ddos.guard|checking your browser/i.test(document.title)""",
                        timeout=30000,
                    )
                    if navigation is not None and navigation.status >= 400:
                        navigation = await page.goto(
                            self._browser_base_url, wait_until="domcontentloaded", timeout=30000
                        )
                    if request.method == "GET" and str(request.url).rstrip("/") == (
                        self._browser_base_url.rstrip("/")
                    ):
                        result = httpx.Response(
                            200 if navigation is None else navigation.status,
                            text=await page.content(),
                            headers={"content-type": "text/html; charset=utf-8"},
                            request=request,
                        )
                    else:
                        # fetch runs inside Chromium, using its TLS stack and cookie jar.
                        # Cookie/Origin/Host are controlled by the browser itself.
                        headers = {
                            key: value
                            for key, value in request.headers.items()
                            if key not in {"cookie", "host", "content-length", "origin", "referer"}
                        }
                        payload = await page.evaluate(
                            """async ({url, method, headers, body}) => {
                                const response = await fetch(url, {
                                    method, headers, credentials: 'include',
                                    body: ['GET', 'HEAD'].includes(method) ? undefined : body,
                                    signal: AbortSignal.timeout(30000)
                                });
                                return {status: response.status,
                                    headers: Object.fromEntries(response.headers.entries()),
                                    body: await response.text()};
                            }""",
                            {
                                "url": str(request.url),
                                "method": request.method,
                                "headers": headers,
                                "body": request.content.decode("utf-8"),
                            },
                        )
                        result = httpx.Response(
                            payload["status"],
                            text=payload["body"],
                            headers={
                                key: value
                                for key, value in payload["headers"].items()
                                if key.lower()
                                not in {"content-encoding", "content-length", "transfer-encoding"}
                            },
                            request=request,
                        )
                    # Preserve expiry, path, Secure and HttpOnly when importing cookies.
                    browser_cookies = await context.cookies()
                    self.cookies.clear()
                    for browser_cookie in browser_cookies:
                        cookie_data: dict[str, Any] = dict(browser_cookie)
                        self.cookies.jar.set_cookie(
                            Cookie(
                                version=0,
                                name=cookie_data["name"],
                                value=cookie_data["value"],
                                port=None,
                                port_specified=False,
                                domain=cookie_data["domain"],
                                domain_specified=cookie_data["domain"].startswith("."),
                                domain_initial_dot=cookie_data["domain"].startswith("."),
                                path=cookie_data["path"],
                                path_specified=True,
                                secure=cookie_data["secure"],
                                expires=int(cookie_data["expires"])
                                if cookie_data["expires"] > 0
                                else None,
                                discard=cookie_data["expires"] <= 0,
                                comment=None,
                                comment_url=None,
                                rest={"HttpOnly": ""} if cookie_data["httpOnly"] else {},
                            )
                        )
                    return result
                finally:
                    await browser.close()
        except PlaywrightTimeoutError as exc:
            raise RuntimeError(_BROWSER_TIMEOUT) from exc
        except PlaywrightError as exc:
            raise RuntimeError(_BROWSER_FAILED) from exc
