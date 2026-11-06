from datetime import date

from pydantic import BaseModel, HttpUrl

from top_journal_sdk._models import APIModel


class EvaluationTagResponse(APIModel):
    id: int
    translate_key: str
    type: str


class EvaluationTagsResponse(APIModel):
    evaluation_tags: list[EvaluationTagResponse]


class EvaluationResponse(APIModel):
    key: str
    date_visit: date
    fio_teach: str
    spec_name: str
    teach_photo: HttpUrl | None


class EvaluationsResponse(APIModel):
    evaluation_list: list[EvaluationResponse]


class EvaluationRequest(BaseModel):
    comment_lesson: str = ""
    comment_teach: str = ""
    key: str
    mark_lesson: int
    mark_teach: int
    tags_lesson: list[int]
    tags_teach: list[int]
