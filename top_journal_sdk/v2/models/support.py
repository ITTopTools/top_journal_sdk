from pydantic import AliasChoices, Field

from top_journal_sdk._models import UnconfirmedResponse


class SupportRequest(UnconfirmedResponse):
    """Fields read by the frontend; unobserved additional fields remain JSON."""

    id: int | str | None = Field(
        default=None, validation_alias=AliasChoices("id", "signal_id", "signalId")
    )
    problem_id: int | None = Field(
        default=None, validation_alias=AliasChoices("problem_id", "problemId")
    )
    status: int | None = None
    priority: int | None = None
    theme: str | None = None
    message: str | None = None
    date_start: str | None = Field(
        default=None, validation_alias=AliasChoices("date_start", "dateStart")
    )
    date_desired: str | None = Field(
        default=None, validation_alias=AliasChoices("date_desired", "dateDesired")
    )
    viewed: bool | None = Field(
        default=None, validation_alias=AliasChoices("viewed", "is_viewed", "isViewed")
    )
