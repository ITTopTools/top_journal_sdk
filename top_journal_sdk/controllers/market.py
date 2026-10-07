from typing import Annotated

from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.market import MarketProductListResponse
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class MarketController(BaseController):
    """
    Market controller.

    Handles retrieval of market products.

    Контроллер маркета.

    Обрабатывает получение товаров маркета.
    """

    @with_auth_refresh
    @get(endpoints.MARKET_PRODUCT_LIST.value)
    async def get_product_list(
        self,
        page: Annotated[int, Query()] = 1,  # pyright: ignore[reportUnusedParameter]
        product_type: Annotated[int | None, Query(alias="type")] = None,  # pyright: ignore[reportUnusedParameter]
    ) -> MarketProductListResponse:
        """
        Get market product list (API responds with an object).

        Получить список товаров маркета (API отвечает объектом).

        Args:
            page: Page number, 1-based / Номер страницы с 1.
            product_type: Product type filter (sent as `type`) / Фильтр типа.

        Returns:
            MarketProductListResponse: Products with total count / Товары с общим количеством.
        """
        ...
