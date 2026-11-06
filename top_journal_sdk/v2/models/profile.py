from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class Phone(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    type: int
    number: str
    is_main: bool


class Payment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    has_any_data: bool
    account_amount: int | None = None
    debt_amount: int | None = None
    next_payment_date: str | None = None
    contract_number: str | None = None
    status: str | None = None


class SocialLink(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    key: str
    name: str
    url: str
    is_required: bool
    is_visible: bool
    is_valid: bool
    required_type: int
    pattern: str


class Profile(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    full_name: str
    first_name: str
    last_name: str
    patronymic: str
    avatar: str | None = None
    level: int
    fill_percentage: int
    is_completed: bool
    email: str | None = None
    phone: str | None = None
    phones: list[Phone]
    birth_date: str | None = None
    address: str | None = None
    study: str | None = None
    azure_login: str | None = None
    form_type: int = 0
    is_email_verified: bool = False
    is_phone_verified: bool = False
    has_pending_data: bool = False
    has_pending_photo: bool = False
    last_approving_status: int = 0
    decline_comment: str | None = None
    social_links: list[SocialLink]
    payment: Payment


class ProfileSettingsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    profile: Profile


class DocumentStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    applicant_passport: bool
    certificate: bool
    certificate086_u: bool
    snils_number: bool
    photo_of_applicant: bool
    registration_certificate: bool
    statuses: dict[str, str]
    details: dict[str, str]
    files: dict[str, str]
    snils_number_value: str | None = None
    has_any_data: bool
    required_completed: int
    required_total: int
    optional_completed: int
    optional_total: int


class DocumentsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    documents: DocumentStatus
