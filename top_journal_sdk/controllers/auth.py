from typing import Annotated

from httpx import Response
from rapid_api_client import PydanticBody, post

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    ResetPasswordRequest,
)
from top_journal_sdk.rapid.client import BaseController


class AuthController(BaseController):
    """
    Authentication controller.

    Manages user authentication and JWT token handling for the journal system.
    Provides secure login functionality with automatic token management
    and session handling for all subsequent API requests.

    Контроллер аутентификации.

    Управляет аутентификацией пользователей и обработкой JWT токенов для системы журнала.
    Предоставляет безопасную функцию входа с автоматическим управлением токенами
    и обработкой сессий для всех последующих API запросов.
    """

    @post(endpoints.AUTH_LOGIN.value)
    async def login(
        self,
        body: Annotated[LoginRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> LoginResponse:
        """
        Authenticate user and obtain access token.

        Performs user authentication using provided credentials and returns
        an access token for subsequent API requests. The token is automatically
        stored and used for all authenticated operations.

        Аутентифицировать пользователя и получить токен доступа.

        Выполняет аутентификацию пользователя с использованием предоставленных учетных данных и возвращает
        токен доступа для последующих API запросов. Токен автоматически
        сохраняется и используется для всех аутентифицированных операций.

        Args:
            body:
                User credentials for authentication including username and password.

                Учетные данные пользователя для аутентификации, включая имя пользователя и пароль.

        Returns:
            LoginResponse:
                Authentication response containing access token and user information.

                Ответ аутентификации, содержащий токен доступа и информацию о пользователе.
        """
        ...

    @post(endpoints.AUTH_REFRESH.value)
    async def refresh(
        self,
        body: Annotated[RefreshTokenRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> LoginResponse:
        """
        Refresh access token using a refresh token.

        Exchanges a valid refresh token for a new access/refresh token pair
        without requiring user credentials.

        Обновить токен доступа с помощью refresh-токена.

        Обменивает действительный refresh-токен на новую пару токенов
        без запроса учетных данных пользователя.

        Args:
            body:
                Refresh token payload.

                Данные с refresh-токеном.

        Returns:
            LoginResponse:
                New access/refresh token pair.

                Новая пара токенов доступа и обновления.
        """
        ...

    @post(endpoints.AUTH_RESET_PASSWORD.value, raise_for_status=True)
    async def post_reset_password_response(
        self,
        body: Annotated[ResetPasswordRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> Response:
        """
        Request a password reset email (raw response).

        Запросить письмо сброса пароля (сырой ответ).
        """
        ...

    async def post_reset_password(self, email: str) -> bool:
        """
        Request a password reset email.

        Запросить письмо сброса пароля. Внимание: отправляет реальное письмо.

        Args:
            email: Account email / Email аккаунта.

        Returns:
            True on success (raises on HTTP errors) / True при успехе.
        """
        response = await self.post_reset_password_response(
            ResetPasswordRequest(email=email)
        )
        return response.is_success
