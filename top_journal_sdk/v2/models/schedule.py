from __future__ import annotations

import datetime as dt

from top_journal_sdk.v2.models._base import V2Model


class ScheduleItem(V2Model):
    id: str
    date: dt.date
    lesson: int
    start_time: dt.time
    end_time: dt.time
    start_minutes: int
    end_minutes: int
    duration_minutes: int
    subject_key: str
    subject_fallback: str
    teacher: str | None = None


class ScheduleResponse(V2Model):
    items: list[ScheduleItem]
