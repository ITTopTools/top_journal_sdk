from typing import Annotated

from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.content import (
    CitiesResponse,
    CityResponse,
    LanguageResponse,
    LanguagesResponse,
    LoginPageStoriesResponse,
    LoginPageStoryResponse,
    NewsListResponse,
    NewsResponse,
    StoriesResponse,
    StoryResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class ContentController(BaseController):
    """
    Content controller.

    Handles retrieval of news, stories, languages and cities.

    Контроллер контента.

    Обрабатывает получение новостей, сторис, языков и городов.
    """

    @with_auth_refresh
    @get(endpoints.NEWS_LATEST.value)
    async def get_latest_news_list(self) -> list[NewsResponse]:
        """
        Get latest news.

        Получить последние новости.

        Returns:
            list[NewsResponse]: News entries / Новости.
        """
        ...

    async def get_latest_news(self) -> NewsListResponse:
        """
        Get latest news in response wrapper.

        Получить последние новости в обертке ответа.

        Returns:
            NewsListResponse: News object / Объект новостей.
        """
        return NewsListResponse(news_list=await self.get_latest_news_list())

    @with_auth_refresh
    @get(endpoints.STORIES_LIST.value)
    async def get_story_list(self) -> list[StoryResponse]:
        """
        Get stories.

        Получить сторис.

        Returns:
            list[StoryResponse]: Stories / Сторис.
        """
        ...

    async def get_stories(self) -> StoriesResponse:
        """
        Get stories in response wrapper.

        Получить сторис в обертке ответа.

        Returns:
            StoriesResponse: Stories object / Объект сторис.
        """
        return StoriesResponse(story_list=await self.get_story_list())

    @with_auth_refresh
    @get(endpoints.STORIES_LOGIN_PAGE.value)
    async def get_login_page_story_list(self) -> list[LoginPageStoryResponse]:
        """
        Get login page stories (public endpoint).

        Получить сторис страницы входа (публичный эндпоинт).

        Returns:
            list[LoginPageStoryResponse]: Login page stories / Сторис входа.
        """
        ...

    async def get_login_page_stories(self) -> LoginPageStoriesResponse:
        """
        Get login page stories in response wrapper.

        Получить сторис страницы входа в обертке ответа.

        Returns:
            LoginPageStoriesResponse: Stories object / Объект сторис.
        """
        return LoginPageStoriesResponse(
            login_page_story_list=await self.get_login_page_story_list()
        )

    @with_auth_refresh
    @get(endpoints.PUBLIC_LANGUAGES.value)
    async def get_language_list(self) -> list[LanguageResponse]:
        """
        Get languages.

        Получить языки.

        Returns:
            list[LanguageResponse]: Languages / Языки.
        """
        ...

    async def get_languages(self) -> LanguagesResponse:
        """
        Get languages in response wrapper.

        Получить языки в обертке ответа.

        Returns:
            LanguagesResponse: Languages object / Объект языков.
        """
        return LanguagesResponse(language_list=await self.get_language_list())

    @with_auth_refresh
    @get(endpoints.PUBLIC_TRANSLATIONS.value)
    async def get_translations(
        self,
        language: Annotated[str, Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> dict[str, str]:
        """
        Get translation map for a language.

        Получить карту переводов для языка.

        Args:
            language: Language code (e.g. ru) / Код языка (например ru).

        Returns:
            dict[str, str]: Translation key-value map / Карта переводов.
        """
        ...

    @with_auth_refresh
    @get(endpoints.PUBLIC_CITIES.value)
    async def get_city_list(self) -> list[CityResponse]:
        """
        Get cities.

        Получить города.

        Returns:
            list[CityResponse]: Cities / Города.
        """
        ...

    async def get_cities(self) -> CitiesResponse:
        """
        Get cities in response wrapper.

        Получить города в обертке ответа.

        Returns:
            CitiesResponse: Cities object / Объект городов.
        """
        return CitiesResponse(city_list=await self.get_city_list())
