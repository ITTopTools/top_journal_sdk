from pydantic import BaseModel


class LoginRequest(BaseModel):
    application_key: str
    username: str
    password: str
    id_city: str | None = None


class LoginResponse(BaseModel):
    access_token: str
