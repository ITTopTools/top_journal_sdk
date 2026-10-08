"""Live-тесты Волны 3: парсинг реальных ответов API в модели SDK.
Требуют TOP_JOURNAL_USERNAME/PASSWORD в env, иначе скипаются.
Марка: live (uv run pytest -m live).

Мутирующие вызовы (смена группы, сброс пароля) здесь НЕ выполняются.
"""

# pyright: reportPrivateUsage=false
# Тест refresh сознательно лезет во внутренности SDK (токены/клиент).

import os

import pytest

from top_journal_sdk import TopJournalSDK

_LIVE_CREDS = bool(
    os.environ.get("TOP_JOURNAL_USERNAME") and os.environ.get("TOP_JOURNAL_PASSWORD")
)

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not _LIVE_CREDS, reason="live creds missing"),
]


async def _login() -> TopJournalSDK:
    sdk = TopJournalSDK(timeout=30.0)
    await sdk.initialize()
    await sdk.login(os.environ["TOP_JOURNAL_USERNAME"], os.environ["TOP_JOURNAL_PASSWORD"])
    return sdk


async def test_live_profile() -> None:
    sdk = await _login()
    try:
        settings = await sdk.profile.get_profile_settings()
        assert settings.id is not None

        achievements = await sdk.profile.get_student_achievements()
        assert isinstance(achievements.student_achievement_list, list)

        fields = await sdk.profile.get_profile_fields()
        assert isinstance(fields.profile_form_list, list)

        group_specs = await sdk.profile.get_group_specs()
        assert len(group_specs.spec_list) > 0

        history_specs = await sdk.profile.get_history_specs()
        assert isinstance(history_specs.spec_list, list)

        forms = await sdk.profile.get_public_forms()
        assert len(forms.profile_form_list) > 0
    finally:
        await sdk.close()


async def test_live_payment() -> None:
    sdk = await _login()
    try:
        index = await sdk.payment.get_payment_index()
        assert index.full_name is not None

        history = await sdk.payment.get_payment_histories()
        assert isinstance(history.payment_history_list, list)

        schedule = await sdk.payment.get_payment_schedules()
        assert isinstance(schedule.payment_schedule_list, list)

        assert await sdk.payment.has_payment_cancellation() is False
    finally:
        await sdk.close()


async def test_live_signal_contacts() -> None:
    sdk = await _login()
    try:
        signals = await sdk.signal.get_signals()
        assert isinstance(signals.signal_list, list)

        problems = await sdk.signal.get_signal_problems()
        assert len(problems.signal_problem_list) > 0

        assert await sdk.signal.has_reference_status() is False

        contacts = await sdk.contacts.get_contacts()
        assert contacts is not None

        assert await sdk.contacts.has_mailing_confirmation() is False
    finally:
        await sdk.close()


async def test_live_reviews_instruction() -> None:
    sdk = await _login()
    try:
        text = await sdk.feedback.get_reviews_instruction()
        assert isinstance(text, str)
    finally:
        await sdk.close()


async def test_live_refresh_rotates_tokens() -> None:
    sdk = await _login()
    try:
        assert sdk._client is not None
        old = sdk._client.headers["Authorization"]
        await sdk._refresh_access_token()
        new = sdk._client.headers["Authorization"]
        assert old != new
        # SDK остается рабочим после refresh.
        user = await sdk.user.get_personal_info()
        assert user.full_name
    finally:
        await sdk.close()
