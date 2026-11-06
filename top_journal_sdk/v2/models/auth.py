from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class LoginRequest(BaseModel):
    """Запрос логина для journalka API v2."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    username: str
    password: str


class LoginResponse(BaseModel):
    """Ответ логина для journalka API v2 (токены в cookies, тело — краткая инфа)."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    user_type: int
    user_role: str


class RefreshResponse(BaseModel):
    """Ответ обновления токена."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    ok: bool
