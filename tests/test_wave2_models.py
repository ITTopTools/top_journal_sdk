"""Unit-тесты моделей Волны 2 на синтетических payload (без сети)."""

from top_journal_sdk.models.content import (
    CityResponse,
    LanguageResponse,
    LoginPageStoryResponse,
    NewsResponse,
    StoryResponse,
)
from top_journal_sdk.models.feedback import (
    AcademyDayCommentRequest,
    AcademyDayResponse,
    SetViewMaterialsRequest,
    SocialReviewResponse,
)
from top_journal_sdk.models.library import (
    LibraryCountResponse,
    LibraryMaterialResponse,
)
from top_journal_sdk.models.market import MarketProductListResponse
from top_journal_sdk.models.portfolio import DesignTeacherResponse, PortfolioResponse
from top_journal_sdk.models.spec import SpecModel


def test_social_review() -> None:
    review = SocialReviewResponse.model_validate(
        {"social_id": 7, "link": "https://example.com/r", "is_visibility": True}
    )
    assert review.social_id == 7
    assert review.comment is None


def test_academy_day() -> None:
    form = AcademyDayResponse.model_validate(
        {"id": 1, "id_city": 5, "evaluation": 2, "default_lang": "ru"}
    )
    assert form.evaluation == 2


def test_academy_day_comment_request() -> None:
    body = AcademyDayCommentRequest(id=1, message="Great!")
    assert body.model_dump() == {"id": 1, "message": "Great!"}


def test_set_view_materials_request() -> None:
    body = SetViewMaterialsRequest(type=1, materials=[1167248, 1167249])
    assert body.model_dump() == {"type": 1, "materials": [1167248, 1167249]}


def test_library_material() -> None:
    material = LibraryMaterialResponse.model_validate(
        {
            "filename": None,
            "url": None,
            "download_url": "https://fs.top-academy.ru/api/v1/files/x",
            "accessibility": {"response_code": None, "last_check": None},
            "material_id": 1167248,
            "theme": "Theme",
            "material_type": 1,
            "is_new_material": True,
            "date": "2026-05-21 10:39:39",
            "sort_date": 1779349179,
        }
    )
    assert material.material_id == 1167248
    assert material.accessibility is not None


def test_library_count() -> None:
    counter = LibraryCountResponse.model_validate(
        {
            "material_type_id": 1,
            "materials_count": 10,
            "new_count": 2,
            "recommended_count": 3,
        }
    )
    assert counter.materials_count == 10


def test_market_product_list() -> None:
    payload = MarketProductListResponse.model_validate(
        {
            "total_count": 1,
            "products_list": [
                {
                    "description": "desc",
                    "vendor_code": "v1",
                    "status": 1,
                    "dynamic_price_status": 1,
                    "id": 18,
                    "title": "title",
                    "quantity": 1,
                    "file_name": "https://fs.top-academy.ru/api/v1/files/x",
                    "url": "https://fs.top-academy.ru/api/v1/files/x",
                    "prices": [{"point_type_id": 1, "points_sum": 2660, "log": []}],
                }
            ],
        }
    )
    assert payload.total_count == 1
    assert payload.products_list[0].prices[0].points_sum == 2660


def test_portfolio() -> None:
    entry = PortfolioResponse.model_validate({"id": 3, "portfolio_title": "title", "mark": 5})
    assert entry.id == 3


def test_design_teacher() -> None:
    teacher = DesignTeacherResponse.model_validate({"id": 1, "fio_teach": "Name"})
    assert teacher.fio_teach == "Name"


def test_spec_model() -> None:
    spec = SpecModel.model_validate(
        {"id": 1033, "name": "Spec", "short_name": "S", "subject_source": None}
    )
    assert spec.id == 1033


def test_news() -> None:
    news = NewsResponse.model_validate(
        {
            "id_bbs": 1,
            "theme": "Theme",
            "time": "2026-10-02 15:03:23",
            "viewed": False,
        }
    )
    assert news.viewed is False


def test_story() -> None:
    story = StoryResponse.model_validate(
        {
            "id": 1,
            "name": "Name",
            "active": 1,
            "show_on_login_page": 0,
            "media_type": "image",
            "created_at": "2026-03-11",
            "updated_at": "2026-03-11",
        }
    )
    assert story.media_type == "image"


def test_login_page_story() -> None:
    story = LoginPageStoryResponse.model_validate({"id": 1, "description": "Desc"})
    assert story.description == "Desc"


def test_language() -> None:
    language = LanguageResponse.model_validate({"name_mystat": "ru_RU", "short_name": "ru"})
    assert language.short_name == "ru"


def test_city() -> None:
    city = CityResponse.model_validate(
        {
            "id_city": 1,
            "prefix": "msk",
            "translate_key": "MOSCOW",
            "timezone_name": "Europe/Moscow",
            "country_code": "RU/RUS",
            "market_status": 1,
            "name": "Moscow",
        }
    )
    assert city.id_city == 1
