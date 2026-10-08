from typing import Annotated

from rapid_api_client import Query, get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.portfolio import (
    DesignTeacherResponse,
    DesignTeachersResponse,
    PortfolioResponse,
    PortfoliosResponse,
)
from top_journal_sdk.models.spec import SpecModel, SpecsResponse
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class PortfolioController(BaseController):
    """
    Portfolio controller.

    Handles retrieval of student portfolios and design references.

    Контроллер портфолио.

    Обрабатывает получение портфолио студентов и дизайн-референсов.
    """

    @with_auth_refresh
    @get(endpoints.PORTFOLIO_LIST.value)
    async def get_portfolio_list(self) -> list[PortfolioResponse]:
        """
        Get portfolio entries.

        Получить работы портфолио.

        Returns:
            list[PortfolioResponse]: Portfolio entries / Работы портфолио.
        """
        ...

    async def get_portfolios(self) -> PortfoliosResponse:
        """
        Get portfolio entries in response wrapper.

        Получить работы портфолио в обертке ответа.

        Returns:
            PortfoliosResponse: Portfolio object / Объект портфолио.
        """
        return PortfoliosResponse(portfolio_list=await self.get_portfolio_list())

    @with_auth_refresh
    @get(endpoints.PORTFOLIO_DESIGN_SPECS.value)
    async def get_design_spec_list(
        self,
        spec_id: Annotated[int, Query(alias="id")],  # pyright: ignore[reportUnusedParameter]
    ) -> list[SpecModel]:
        """
        Get design specs for a portfolio entry.

        Получить предметы для дизайна работы портфолио.

        Args:
            spec_id: Portfolio entry ID (sent as `id`) / ID работы (как `id`).

        Returns:
            list[SpecModel]: Design specs / Предметы дизайна.
        """
        ...

    async def get_design_specs(self, spec_id: int) -> SpecsResponse:
        """
        Get design specs in response wrapper.

        Получить предметы дизайна в обертке ответа.

        Args:
            spec_id: Portfolio entry ID / ID работы портфолио.

        Returns:
            SpecsResponse: Specs object / Объект предметов.
        """
        return SpecsResponse(spec_list=await self.get_design_spec_list(spec_id))

    @with_auth_refresh
    @get(endpoints.PORTFOLIO_DESIGN_TEACHERS.value)
    async def get_design_teacher_list(self) -> list[DesignTeacherResponse]:
        """
        Get portfolio design teachers.

        Получить преподавателей для дизайна портфолио.

        Returns:
            list[DesignTeacherResponse]: Teachers / Преподаватели.
        """
        ...

    async def get_design_teachers(self) -> DesignTeachersResponse:
        """
        Get portfolio design teachers in response wrapper.

        Получить преподавателей дизайна в обертке ответа.

        Returns:
            DesignTeachersResponse: Teachers object / Объект преподавателей.
        """
        return DesignTeachersResponse(design_teacher_list=await self.get_design_teacher_list())
