from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class CheckCancellationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    status: int
    is_cancellation_active: bool


class EmailConfirmationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    email_confirmation: str | None = None


class LessonEvaluationPendingResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    lesson_evaluation_pending_count: int


class OpenedInterviewResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    opened_interview: str | None = None


class SignalsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    signals_list: list[dict[str, Any]]
