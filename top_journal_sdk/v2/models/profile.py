from __future__ import annotations

import datetime as dt

from pydantic import JsonValue

from top_journal_sdk._models import UnconfirmedResponse
from top_journal_sdk.v2.models._base import V2Model


class Phone(V2Model):
    id: str
    type: int
    number: str
    is_main: bool


class Payment(V2Model):
    has_any_data: bool
    account_amount: int | None = None
    debt_amount: int | None = None
    next_payment_date: dt.date | None = None
    contract_number: str | None = None
    status: str | None = None


class SocialLink(V2Model):
    id: str
    key: str
    name: str
    url: str
    is_required: bool
    is_visible: bool
    is_valid: bool
    required_type: int
    pattern: str


class DeclineComment(V2Model):
    message: str


class Profile(V2Model):
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
    birth_date: dt.date | None = None
    address: str | None = None
    study: str | None = None
    azure_login: str | None = None
    form_type: int = 0
    is_email_verified: bool = False
    is_phone_verified: bool = False
    has_pending_data: bool = False
    has_pending_photo: bool = False
    last_approving_status: int = 0
    decline_comment: DeclineComment | str | None = None
    social_links: list[SocialLink]
    payment: Payment


class ProfileSettingsResponse(V2Model):
    profile: Profile


class DocumentStatus(V2Model):
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


class DocumentsResponse(V2Model):
    documents: DocumentStatus


class DocumentFile(V2Model):
    name: str
    path: str


class DocumentModeration(V2Model):
    status: bool | None = None
    comment: str | None = None


class DocumentField(V2Model):
    id: int
    name: str
    type: str
    code: str
    translation_key: str
    text_value: str
    files: list[DocumentFile]
    options: dict[str, JsonValue]
    moderation: DocumentModeration | None


class DocumentFieldsResponse(V2Model):
    fields: list[DocumentField]


class ChangeGroupResponse(UnconfirmedResponse):
    """Group-change acknowledgement; unconfirmed, losslessly preserved JSON."""
