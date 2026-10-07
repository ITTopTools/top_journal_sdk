# pyright: reportPrivateUsage=false
# Тесты сознательно проверяют внутреннее состояние SDK (кеш контроллеров/клиент).
import httpx
import pytest

from top_journal_sdk import DEFAULT_TIMEOUT, TopJournalSDK

HTML = '<html><head><script src="/static/js/app.abc123.js"></script></head></html>'
JS = 'var x; o.authModel = new r.AuthModel("MOCKKEY");'


def _mock_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith(".js"):
            return httpx.Response(200, text=JS)
        if request.method == "POST":
            return httpx.Response(200, json={"access_token": "TOKEN123"})
        return httpx.Response(200, text=HTML)

    return httpx.MockTransport(handler)


async def test_initialize_idempotent() -> None:
    sdk = TopJournalSDK()
    await sdk.initialize()
    client = sdk._client
    await sdk.initialize()
    assert sdk._client is client
    await sdk.close()


async def test_close_resets_controllers() -> None:
    sdk = TopJournalSDK()
    await sdk.initialize()
    assert sdk.user is sdk.user
    await sdk.close()
    assert sdk._client is None
    assert sdk._user_info_controller is None
    # Повторная инициализация после close работает
    await sdk.initialize()
    assert sdk._client is not None
    assert sdk.user is not None
    await sdk.close()


async def test_controller_factory_caches() -> None:
    sdk = TopJournalSDK()
    await sdk.initialize()
    assert sdk.auth is sdk.auth
    assert sdk.grades is sdk.grades
    assert sdk.attendance is not sdk.grades
    await sdk.close()


async def test_guards_without_initialize() -> None:
    sdk = TopJournalSDK()
    with pytest.raises(RuntimeError):
        sdk.user
    with pytest.raises(RuntimeError):
        sdk.set_auth_token("x")
    with pytest.raises(RuntimeError):
        await sdk.login("user", "pass")


async def test_timeout_and_headers() -> None:
    async with TopJournalSDK(
        timeout=5.0, user_agent="TestAgent/1.0", extra_headers={"X-Test": "1"}
    ) as sdk:
        assert sdk._client is not None
        assert sdk._client.timeout == httpx.Timeout(5.0)
        assert sdk._client.headers["User-Agent"] == "TestAgent/1.0"
        assert sdk._client.headers["X-Test"] == "1"


async def test_defaults() -> None:
    async with TopJournalSDK() as sdk:
        assert sdk._client is not None
        assert sdk._client.timeout == httpx.Timeout(DEFAULT_TIMEOUT)
        assert "Chrome" in sdk._client.headers["User-Agent"]


async def test_login_end_to_end_on_mocks() -> None:
    sdk = TopJournalSDK()
    await sdk.initialize()
    assert sdk._client is not None
    sdk._client._transport = _mock_transport()
    token = await sdk.login("user", "pass")
    assert token == "TOKEN123"
    assert sdk._client.headers["Authorization"] == "Bearer TOKEN123"
    await sdk.close()
