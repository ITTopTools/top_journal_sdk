from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class ScheduleItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    date: str
    lesson: int
    start_time: str
    end_time: str
    start_minutes: int
    end_minutes: int
    duration_minutes: int
    subject_key: str
    subject_fallback: str
    teacher: str | None = None


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[ScheduleItem]
