from pydantic import BaseModel


class LoginRequest(BaseModel):
    application_key: str
    username: str
    password: str
    id_city: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in_access: int = 0
    expires_in_refresh: int = 0


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ResetPasswordRequest(BaseModel):
    """Запрос сброса пароля.

    Password reset request.

    Поле по форме фронта (одно поле E-mail).
    """

    email: str
