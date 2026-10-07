import datetime

from pydantic import BaseModel, field_validator


class LegacyPaymentResponse(BaseModel):
    """Устаревшие данные оплаты.

    Legacy payment data.
    """

    message_type: int | None = None
    amount: float | None = None
    date_start: str | None = None
    pay_date_start: str | None = None


class PaymentDetailsResponse(BaseModel):
    """Детали активной оплаты.

    Active payment details.
    """

    id: int | None = None
    fio_stud: str | None = None
    one_c_code: str | None = None
    date_start: str | None = None
    amount_debt: float | None = None
    pay_date_start: str | None = None
    amount_next: float | None = None
    purpose_of_payment: str | None = None
    okpo: str | None = None
    settlement_account: str | None = None
    mfo: str | None = None
    bank_name: str | None = None
    organization_name: str | None = None
    organization_address: str | None = None
    organization_phone: str | None = None
    organization_status: int | None = None
    payer_full_name: str | None = None
    amount_in_words: str | None = None
    amount_to_pay: float | None = None
    updated_at: str | None = None

    @field_validator("organization_status", mode="before")
    @classmethod
    def _empty_string_to_none(cls, value: object) -> object:
        # Бэкенд присылает "" вместо null для пустых int-полей.
        return None if value == "" else value


class PaymentIndexResponse(BaseModel):
    """Данные оплаты студента.

    Student payment data.
    """

    instruction_link: str | None = None
    mobile_instruction_link: str | None = None
    online_link: str | None = None
    full_name: str | None = None
    city_id: int | None = None
    legacy_payment: LegacyPaymentResponse | None = None
    payment: PaymentDetailsResponse | None = None
    one_c_code: str | None = None
    has_invoice_access: bool | None = None
    has_add_invoice_access: bool | None = None
    online_link_has: bool | None = None
    contract_offer: str | None = None


class PaymentHistoryResponse(BaseModel):
    """Запись истории оплат.

    Payment history entry.
    """

    date: datetime.date | None = None
    amount: float | None = None
    description: str | None = None
    type: int | None = None


class PaymentHistoriesResponse(BaseModel):
    payment_history_list: list[PaymentHistoryResponse]


class PaymentScheduleResponse(BaseModel):
    """Запись графика оплат.

    Payment schedule entry.
    """

    id: int | None = None
    description: str | None = None
    price: float | None = None
    payment_date: datetime.date | None = None
    status: int | None = None


class PaymentSchedulesResponse(BaseModel):
    payment_schedule_list: list[PaymentScheduleResponse]
