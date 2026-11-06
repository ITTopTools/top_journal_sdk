from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel
from top_journal_sdk.v2.models._base import V2Model


class LoginRequest(BaseModel):
    """Запрос логина для journalka API v2."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    username: str
    password: str


class LoginResponse(V2Model):
    """Ответ логина для journalka API v2 (токены в cookies, тело — краткая инфа)."""

    user_type: int
    user_role: str


class RefreshResponse(V2Model):
    """Ответ обновления токена."""

    ok: bool
