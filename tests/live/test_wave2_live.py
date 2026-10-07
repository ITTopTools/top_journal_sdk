"""Live-тесты Волны 2: парсинг реальных ответов API в модели SDK.

Требуют TOP_JOURNAL_USERNAME/PASSWORD в env, иначе скипаются.
Марка: live (uv run pytest -m live).

Мутирующие POST (screen-review, comment) здесь НЕ вызываются —
только shape-тесты тел (см. tests/test_wave2_models.py).
"""

import os

import pytest

from top_journal_sdk import TopJournalSDK
from top_journal_sdk.exceptions import DataNotFoundError

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        not os.environ.get("TOP_JOURNAL_USERNAME")
        or not os.environ.get("TOP_JOURNAL_PASSWORD"),
        reason="live creds missing",
    ),
]


async def _login() -> TopJournalSDK:
    sdk = TopJournalSDK(timeout=30.0)
    await sdk.initialize()
    await sdk.login(
        os.environ["TOP_JOURNAL_USERNAME"], os.environ["TOP_JOURNAL_PASSWORD"]
    )
    return sdk


async def test_live_feedback_wave2() -> None:
    sdk = await _login()
    try:
        reviews = await sdk.feedback.get_social_reviews()
        assert isinstance(reviews.social_review_list, list)
    finally:
        await sdk.close()


@pytest.mark.xfail(
    strict=True, reason="set-view payload under discovery (server 422 on mined shape)"
)
async def test_live_set_view_materials() -> None:
    sdk = await _login()
    try:
        materials = await sdk.library.get_library_materials(
            material_type=1, recommended_type=1
        )
        assert len(materials.library_material_list) > 0
        material_id = materials.library_material_list[0].material_id
        assert material_id is not None
        assert await sdk.feedback.post_set_view_materials(1, [material_id]) is True
    finally:
        await sdk.close()


async def test_live_academy_day_unknown_id() -> None:
    sdk = await _login()
    try:
        # Валидный evaluation id неизвестен; фиксируем поведение на невалидном.
        with pytest.raises(DataNotFoundError):
            await sdk.feedback.get_academy_day(evaluation=1)
    finally:
        await sdk.close()


async def test_live_library_market() -> None:
    sdk = await _login()
    try:
        materials = await sdk.library.get_library_materials(
            material_type=1, recommended_type=1
        )
        assert len(materials.library_material_list) > 0

        counts = await sdk.library.get_library_counts()
        assert isinstance(counts.library_count_list, list)

        assert await sdk.library.has_opened_interview() is False

        products = await sdk.market.get_product_list(page=1, product_type=0)
        assert products.total_count >= 0
        assert isinstance(products.products_list, list)
    finally:
        await sdk.close()


async def test_live_portfolio() -> None:
    sdk = await _login()
    try:
        portfolios = await sdk.portfolio.get_portfolios()
        assert len(portfolios.portfolio_list) > 0

        teachers = await sdk.portfolio.get_design_teachers()
        assert isinstance(teachers.design_teacher_list, list)

        specs = await sdk.portfolio.get_design_specs(
            spec_id=portfolios.portfolio_list[0].id
        )
        assert isinstance(specs.spec_list, list)
    finally:
        await sdk.close()


async def test_live_content() -> None:
    sdk = await _login()
    try:
        news = await sdk.content.get_latest_news()
        assert isinstance(news.news_list, list)

        stories = await sdk.content.get_stories()
        assert isinstance(stories.story_list, list)

        login_stories = await sdk.content.get_login_page_stories()
        assert isinstance(login_stories.login_page_story_list, list)

        languages = await sdk.content.get_languages()
        assert len(languages.language_list) > 0

        translations = await sdk.content.get_translations(language="ru")
        assert len(translations) > 0

        cities = await sdk.content.get_cities()
        assert len(cities.city_list) > 0
    finally:
        await sdk.close()
