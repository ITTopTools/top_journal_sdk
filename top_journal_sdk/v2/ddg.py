from __future__ import annotations

import importlib.util
import logging
from contextlib import suppress

__all__ = ["DDG_COOKIE_NAMES", "DdgCookieManager"]

logger = logging.getLogger(__name__)

# Имена кук, которые устанавливает DDoS-Guard при посещении сайта через браузер.
DDG_COOKIE_NAMES = ("__ddg1_", "__ddg8_", "__ddg9_", "__ddg10_")

_PLAYWRIGHT_NOT_INSTALLED = (
    "Playwright не установлен. Установите зависимость [browser] "
    "или передайте __ddg* куки вручную через set_ddg_cookies()."
)
_PLAYWRIGHT_FAILED = (
    "Не удалось получить __ddg* куки через Playwright. "
    "Проверьте, что Chromium установлен (`playwright install chromium`), "
    "или передайте куки вручную через set_ddg_cookies()."
)


def _is_ddg_cookie(name: str) -> bool:
    return name.startswith("__ddg") or name == "ddg_last_challenge"


class DdgCookieManager:
    """
    Управляет куками DDoS-Guard (__ddg*) для journalka.top-academy.ru.

    Куки хранятся только в памяти SDK. Их можно:
    - передать вручную через set_ddg_cookies() (если браузер недоступен),
    - получить автоматически через refresh_via_playwright() (запускает браузер).

    При неудачном запросе (401) SDK может вызвать refresh_via_playwright()
    для обновления кук и повторить запрос.
    """

    def __init__(self, *, auto_refresh: bool = True) -> None:
        self._cookies: dict[str, str] = {}
        self._auto_refresh = auto_refresh
        self._playwright_available = importlib.util.find_spec("playwright") is not None

    @property
    def auto_refresh(self) -> bool:
        return self._auto_refresh

    @property
    def cookies(self) -> dict[str, str]:
        """Возвращает копию текущих __ddg* кук."""
        return dict(self._cookies)

    @property
    def has_cookies(self) -> bool:
        """True, если есть хотя бы одна __ddg* кука."""
        return bool(self._cookies)

    def set_ddg_cookies(self, cookies: dict[str, str]) -> None:
        """
        Установить __ddg* куки вручную (из браузера, DevTools и т.д.).

        Пример:
            manager.set_ddg_cookies({
                "__ddg1_": "...",
                "__ddg8_": "...",
                "__ddg9_": "...",
                "__ddg10_": "...",
            })
        """
        filtered = {k: v for k, v in cookies.items() if _is_ddg_cookie(k)}
        self._cookies.update(filtered)

    def get_cookie_header(self) -> str:
        """Вернуть куки в формате заголовка Cookie."""
        if not self._cookies:
            return ""
        return "; ".join(f"{k}={v}" for k, v in self._cookies.items())

    async def refresh_via_playwright(
        self, base_url: str = "https://journalka.top-academy.ru"
    ) -> None:
        """
        Запустить Playwright (headless Chromium), перейти на базовый URL,
        чтобы DDoS-Guard установил __ddg* куки, и извлечь их.

        Требует установленную зависимость playwright и браузер Chromium.
        """
        if not self._playwright_available:
            raise RuntimeError(_PLAYWRIGHT_NOT_INSTALLED)

        from playwright.async_api import Error as PlaywrightError
        from playwright.async_api import async_playwright

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                try:
                    context = await browser.new_context(
                        viewport={"width": 1366, "height": 900},
                        user_agent=(
                            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
                        ),
                    )
                    page = await context.new_page()

                    await page.goto(base_url, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(5000)

                    # Также заходим в кабинет, чтобы __ddg* куки точно применились.
                    with suppress(PlaywrightError):
                        await page.goto(
                            base_url + "/ru/main/dashboard",
                            wait_until="domcontentloaded",
                            timeout=15000,
                        )
                        await page.wait_for_timeout(3000)

                    for cookie in await context.cookies():
                        name = cookie.get("name")
                        value = cookie.get("value")
                        if name is not None and _is_ddg_cookie(name) and value is not None:
                            self._cookies[name] = value
                finally:
                    await browser.close()
        except PlaywrightError as exc:
            logger.debug("Playwright failed to obtain DDG cookies", exc_info=True)
            raise RuntimeError(_PLAYWRIGHT_FAILED) from exc

    def should_auto_refresh(self) -> bool:
        return self._auto_refresh and self._playwright_available
