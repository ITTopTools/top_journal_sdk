from rapid_api_client import get

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.user import UserResponse
from journal_sdk.rapid.client import BaseController


class UserInfoController(BaseController):
    """
    Контроллер для работы с базовой информацией о пользователе.

    Controller for managing basic user information.

    Предоставляет методы для получения основной информации о пользователе.

    Provides methods for retrieving basic user information.
    """

    @get(endpoints.USER_PERSONAL_INFO.value)
    async def get_personal_info(self) -> UserResponse:
        """
        Получает личную информацию пользователя из системы журнала.

        Retrieves user personal information from the journal system.

        Returns:
            User:
                Объект с информацией о пользователе.

                User information object.
        """
        ...
