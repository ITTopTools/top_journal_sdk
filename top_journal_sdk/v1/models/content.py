import datetime

from pydantic import HttpUrl

from top_journal_sdk._models import APIModel


class NewsResponse(APIModel):
    """Новость.

    News entry.
    """

    id_bbs: int
    theme: str | None = None
    time: datetime.datetime | None = None
    viewed: bool | None = None


class NewsListResponse(APIModel):
    news_list: list[NewsResponse]


class StoryResponse(APIModel):
    """Сторис.

    Story entry.
    """

    id: int
    name: str | None = None
    description: str | None = None
    active: int | None = None
    show_on_login_page: int | None = None
    url: HttpUrl | None = None
    thumbnail_url: HttpUrl | None = None
    media_url: HttpUrl | None = None
    media_type: str | None = None
    created_by: int | None = None
    updated_by: int | None = None
    created_at: datetime.date | None = None
    updated_at: datetime.date | None = None


class StoriesResponse(APIModel):
    story_list: list[StoryResponse]


class LoginPageStoryResponse(APIModel):
    """Сторис страницы входа.

    Login page story entry.
    """

    id: int
    url: HttpUrl | None = None
    thumbnail_url: HttpUrl | None = None
    description: str | None = None


class LoginPageStoriesResponse(APIModel):
    login_page_story_list: list[LoginPageStoryResponse]


class LanguageResponse(APIModel):
    """Язык.

    Language entry.
    """

    name_mystat: str
    short_name: str


class LanguagesResponse(APIModel):
    language_list: list[LanguageResponse]


class CityResponse(APIModel):
    """Город.

    City entry.
    """

    id_city: int
    prefix: str | None = None
    translate_key: str | None = None
    timezone_name: str | None = None
    country_code: str | None = None
    market_status: int | None = None
    name: str | None = None


class CitiesResponse(APIModel):
    city_list: list[CityResponse]
