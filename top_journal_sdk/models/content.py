import datetime

from pydantic import BaseModel, HttpUrl


class NewsResponse(BaseModel):
    """Новость.

    News entry.
    """

    id_bbs: int
    theme: str | None = None
    time: datetime.datetime | None = None
    viewed: bool | None = None


class NewsListResponse(BaseModel):
    news_list: list[NewsResponse]


class StoryResponse(BaseModel):
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


class StoriesResponse(BaseModel):
    story_list: list[StoryResponse]


class LoginPageStoryResponse(BaseModel):
    """Сторис страницы входа.

    Login page story entry.
    """

    id: int
    url: HttpUrl | None = None
    thumbnail_url: HttpUrl | None = None
    description: str | None = None


class LoginPageStoriesResponse(BaseModel):
    login_page_story_list: list[LoginPageStoryResponse]


class LanguageResponse(BaseModel):
    """Язык.

    Language entry.
    """

    name_mystat: str
    short_name: str


class LanguagesResponse(BaseModel):
    language_list: list[LanguageResponse]


class CityResponse(BaseModel):
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


class CitiesResponse(BaseModel):
    city_list: list[CityResponse]
