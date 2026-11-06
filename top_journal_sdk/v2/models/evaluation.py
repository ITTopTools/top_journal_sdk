from datetime import date, datetime

from top_journal_sdk._models import APIModel
from top_journal_sdk.v2.models._base import V2Model


class LessonEvaluationItem(APIModel):
    key: str
    date_visit: date
    fio_teach: str
    spec_name: str
    teach_photo: str | None


class ResponseMeta(V2Model):
    requested_at: datetime


class LessonEvaluationsResponse(V2Model):
    items: list[LessonEvaluationItem]
    meta: ResponseMeta
