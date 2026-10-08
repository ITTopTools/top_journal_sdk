from httpx import Response
from rapid_api_client import get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.contacts import ContactsResponse
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class ContactsController(BaseController):
    """
    Contacts controller.

    Handles retrieval of branch contacts and mailing confirmation.

    Контроллер контактов.

    Обрабатывает получение контактов филиала и подтверждения рассылки.
    """

    @with_auth_refresh
    @get(endpoints.CONTACTS_INDEX.value)
    async def get_contacts(self) -> ContactsResponse:
        """
        Get branch contacts.

        Получить контакты филиала.

        Returns:
            ContactsResponse: Branch contacts / Контакты филиала.
        """
        ...

    @with_auth_refresh
    @get(endpoints.CONTACTS_CHECK_CONFIRMATION.value, raise_for_status=True)
    async def get_confirmation_check_response(self) -> Response:
        """
        Check mailing confirmation (raw response, 204 when empty).

        Проверить подтверждение рассылки (сырой ответ, 204 если пусто).
        """
        ...

    async def has_mailing_confirmation(self) -> bool:
        """
        Check whether mailing confirmation exists.

        Проверить наличие подтверждения рассылки.

        Returns:
            True when confirmation data exists / True если данные есть.
        """
        response: Response = await self.get_confirmation_check_response()
        return response.status_code == 200
