from httpx import Response
from rapid_api_client import get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.signal import (
    SignalProblemResponse,
    SignalProblemsResponse,
    SignalResponse,
    SignalsResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class SignalController(BaseController):
    """
    Signal controller.

    Handles retrieval of student signals and problems.

    Контроллер сигналов.

    Обрабатывает получение сигналов и проблем студента.
    """

    @with_auth_refresh
    @get(endpoints.SIGNAL_LIST.value)
    async def get_signal_list(self) -> list[SignalResponse]:
        """
        Get student signals.

        Получить сигналы студента.

        Returns:
            list[SignalResponse]: Signals / Сигналы.
        """
        ...

    async def get_signals(self) -> SignalsResponse:
        """
        Get student signals in response wrapper.

        Получить сигналы студента в обертке ответа.

        Returns:
            SignalsResponse: Signals object / Объект сигналов.
        """
        return SignalsResponse(signal_list=await self.get_signal_list())

    @with_auth_refresh
    @get(endpoints.SIGNAL_PROBLEMS.value)
    async def get_signal_problem_list(self) -> list[SignalProblemResponse]:
        """
        Get signal problems.

        Получить список проблем для сигналов.

        Returns:
            list[SignalProblemResponse]: Problems / Проблемы.
        """
        ...

    async def get_signal_problems(self) -> SignalProblemsResponse:
        """
        Get signal problems in response wrapper.

        Получить проблемы сигналов в обертке ответа.

        Returns:
            SignalProblemsResponse: Problems object / Объект проблем.
        """
        return SignalProblemsResponse(signal_problem_list=await self.get_signal_problem_list())

    @with_auth_refresh
    @get(endpoints.SIGNAL_REFERENCE_STATUS.value, raise_for_status=True)
    async def get_reference_status_response(self) -> Response:
        """
        Get reference status (raw response, 204 when empty).

        Получить статус справки (сырой ответ, 204 если пусто).
        """
        ...

    async def has_reference_status(self) -> bool:
        """
        Check whether a reference status exists.

        Проверить наличие статуса справки.

        Returns:
            True when status data exists / True если данные есть.
        """
        response: Response = await self.get_reference_status_response()
        return response.status_code == 200
