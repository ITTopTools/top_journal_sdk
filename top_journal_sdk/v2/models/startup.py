from __future__ import annotations

from pydantic import AliasChoices, Field

from top_journal_sdk._models import UnconfirmedResponse
from top_journal_sdk.v2.models._base import V2Model
from top_journal_sdk.v2.models.support import SupportRequest


class Signal(SupportRequest):
    """Unconfirmed API object; all JSON fields are preserved."""


class CheckCancellationResponse(V2Model):
    status: int
    is_cancellation_active: bool


class EmailConfirmation(V2Model):
    delay_count: int | None = Field(
        default=None, validation_alias=AliasChoices("delayCount", "delay_count")
    )
    max_delay_count: int | None = Field(
        default=None, validation_alias=AliasChoices("maxDelayCount", "max_delay_count")
    )


class OpenedInterview(EmailConfirmation):
    id: int | str | None = None
    message_type: int | None = Field(
        default=None, validation_alias=AliasChoices("messageType", "message_type")
    )


class EmailConfirmationResponse(V2Model):
    email_confirmation: EmailConfirmation | None = None


class LessonEvaluationPendingResponse(V2Model):
    lesson_evaluation_pending_count: int


class OpenedInterviewResponse(V2Model):
    opened_interview: OpenedInterview | None = None


class SignalsResponse(V2Model):
    signals_list: list[Signal]


class DelayInterviewResponse(UnconfirmedResponse):
    """Experimental acknowledgement with unconfirmed JSON schema."""


class DelayEmailConfirmationResponse(UnconfirmedResponse):
    """Acknowledgement; response fields have not yet been observed."""
