# pyright: reportPrivateUsage=false
# Тесты сознательно лезут в protected-парсеры ApplicationKey.
import httpx
import pytest

import top_journal_sdk.exceptions as E
from top_journal_sdk.utils.app_key import ApplicationKey

HTML = '<html><head><script src="/static/js/app.abc123.js"></script></head></html>'
JS = 'var x; o.authModel = new r.AuthModel("APPKEY123");'


def test_js_url_relative() -> None:
    key = ApplicationKey("https://journal.top-academy.ru/")
    assert (
        key._get_js_url(HTML)
        == "https://journal.top-academy.ru/static/js/app.abc123.js"
    )


def test_js_url_absolute() -> None:
    html = '<html><head><script src="https://cdn.test/app.9.js"></script></head></html>'
    key = ApplicationKey("https://journal.top-academy.ru/")
    assert key._get_js_url(html) == "https://cdn.test/app.9.js"


def test_js_url_missing_src() -> None:
    html = "<html><head><script>var a = 1;</script></head></html>"
    key = ApplicationKey("https://journal.top-academy.ru/")
    assert key._get_js_url(html) == ""


def test_js_url_no_scripts() -> None:
    key = ApplicationKey("https://journal.top-academy.ru/")
    assert key._get_js_url("<html></html>") == ""


def test_extract_key() -> None:
    key = ApplicationKey("https://journal.top-academy.ru/")
    assert key._get_app_key(JS) == "APPKEY123"


def test_extract_key_missing() -> None:
    key = ApplicationKey("https://journal.top-academy.ru/")
    assert key._get_app_key("var a = 1;") == ""


def _transport(
    html: str = HTML, js: str = JS, root_status: int = 200
) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith(".js"):
            return httpx.Response(200, text=js)
        return httpx.Response(root_status, text=html)

    return httpx.MockTransport(handler)


async def test_get_key_with_injected_client() -> None:
    async with httpx.AsyncClient(transport=_transport()) as client:
        key = ApplicationKey("https://journal.top-academy.ru/", client=client)
        assert await key.get_key() == "APPKEY123"
        # Кеш: второй вызов без сети
        assert await key.get_key() == "APPKEY123"
        assert not client.is_closed


async def test_get_key_creates_internal_client() -> None:
    key = ApplicationKey("https://journal.top-academy.ru/", timeout=7.5)
    assert key.timeout == 7.5
    # Без сети проверить нечего — создание клиента lazily внутри get_key.


async def test_get_key_no_script_returns_empty() -> None:
    async with httpx.AsyncClient(transport=_transport(html="<html></html>")) as client:
        key = ApplicationKey("https://journal.top-academy.ru/", client=client)
        assert await key.get_key() == ""


async def test_get_key_http_error_mapped() -> None:
    async with httpx.AsyncClient(transport=_transport(root_status=500)) as client:
        key = ApplicationKey("https://journal.top-academy.ru/", client=client)
        with pytest.raises(E.InternalServerError):
            await key.get_key()


async def test_get_key_timeout_mapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("boom")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        key = ApplicationKey("https://journal.top-academy.ru/", client=client)
        with pytest.raises(E.RequestTimeoutError):
            await key.get_key()
