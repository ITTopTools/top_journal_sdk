from pydantic import Field, HttpUrl

from top_journal_sdk._models import APIModel


class MarketProductPriceResponse(APIModel):
    """Цена товара маркета в баллах.

    Market product price in points.
    """

    point_type_id: int
    points_sum: int
    log: list[str]


class MarketProductResponse(APIModel):
    """Товар маркета.

    Market product.
    """

    description: str | None = None
    vendor_code: str | None = None
    status: int | None = None
    dynamic_price_status: int | None = None
    id: int | None = None
    title: str | None = None
    quantity: int | None = None
    file_name: HttpUrl | None = None
    url: HttpUrl | None = None
    prices: list[MarketProductPriceResponse] = Field(
        default_factory=list[MarketProductPriceResponse]
    )


class MarketProductListResponse(APIModel):
    """Список товаров маркета (форма ответа API — объект).

    Market product list (API responds with an object).
    """

    total_count: int
    products_list: list[MarketProductResponse]
