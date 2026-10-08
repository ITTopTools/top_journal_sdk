from httpx import Response
from rapid_api_client import get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.payment import (
    PaymentHistoriesResponse,
    PaymentHistoryResponse,
    PaymentIndexResponse,
    PaymentScheduleResponse,
    PaymentSchedulesResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class PaymentController(BaseController):
    """
    Payment controller (read-only).

    Handles retrieval of payment data, history and schedules.
    No money-moving operations are exposed.

    Контроллер оплаты (только чтение).

    Обрабатывает получение данных оплаты, истории и графиков.
    Денежные операции не предоставляются.
    """

    @with_auth_refresh
    @get(endpoints.PAYMENT_INDEX.value)
    async def get_payment_index(self) -> PaymentIndexResponse:
        """
        Get student payment data.

        Получить данные оплаты студента.

        Returns:
            PaymentIndexResponse: Payment data / Данные оплаты.
        """
        ...

    @with_auth_refresh
    @get(endpoints.PAYMENT_HISTORY.value)
    async def get_payment_history_list(self) -> list[PaymentHistoryResponse]:
        """
        Get payment history.

        Получить историю оплат.

        Returns:
            list[PaymentHistoryResponse]: History entries / Записи истории.
        """
        ...

    async def get_payment_histories(self) -> PaymentHistoriesResponse:
        """
        Get payment history in response wrapper.

        Получить историю оплат в обертке ответа.

        Returns:
            PaymentHistoriesResponse: History object / Объект истории.
        """
        return PaymentHistoriesResponse(payment_history_list=await self.get_payment_history_list())

    @with_auth_refresh
    @get(endpoints.PAYMENT_SCHEDULE.value)
    async def get_payment_schedule_list(self) -> list[PaymentScheduleResponse]:
        """
        Get payment schedule.

        Получить график оплат.

        Returns:
            list[PaymentScheduleResponse]: Schedule entries / Записи графика.
        """
        ...

    async def get_payment_schedules(self) -> PaymentSchedulesResponse:
        """
        Get payment schedule in response wrapper.

        Получить график оплат в обертке ответа.

        Returns:
            PaymentSchedulesResponse: Schedule object / Объект графика.
        """
        return PaymentSchedulesResponse(
            payment_schedule_list=await self.get_payment_schedule_list()
        )

    @with_auth_refresh
    @get(endpoints.PAYMENT_CHECK_CANCELLATION.value, raise_for_status=True)
    async def get_cancellation_check_response(self) -> Response:
        """
        Check payment cancellation state (raw response, 204 when empty).

        Проверить состояние отмены оплаты (сырой ответ, 204 если пусто).
        """
        ...

    async def has_payment_cancellation(self) -> bool:
        """
        Check whether a payment cancellation exists.

        Проверить наличие отмены оплаты.

        Returns:
            True when cancellation data exists / True если данные есть.
        """
        response: Response = await self.get_cancellation_check_response()
        return response.status_code == 200
